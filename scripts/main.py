from argparse import Namespace
import os
import signal
import sys
import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed, Future
from queue import Queue
from tqdm import tqdm
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from jpg2png import (
    Converter,
    file_generator,
    configure_logging,
    handle_signal,
)
from jpg2png.config import parse_arguments

def dynamic_thread_adjustment(
    executor: ThreadPoolExecutor, queue: Queue, shutdown_event: threading.Event, threshold: int = 10
) -> None:
    """
    Adjust the number of threads dynamically based on the system load.

    Args:
        executor (ThreadPoolExecutor): Thread pool executor to adjust.
        queue (Queue): Queue to monitor for task count.
        shutdown_event (threading.Event): Event to signal shutdown.
        threshold (int): Threshold for adjusting the number of threads.
    """
    while not shutdown_event.is_set():
        time.sleep(5)
        queue_size = queue.qsize()
        cpu_count: int = os.cpu_count() or 1
        if queue_size > threshold and executor._max_workers < cpu_count:
            executor._max_workers += 1
            logging.info(msg=f"Increased number of threads to: {executor._max_workers}")
        elif queue_size < threshold and executor._max_workers > 1:
            executor._max_workers -= 1
            logging.info(msg=f"Decreased number of threads to: {executor._max_workers}")

def main() -> None:
    args: Namespace = parse_arguments()
    configure_logging(args.log_level, "error_log.txt")

    if not os.path.isdir(args.directory):
        logging.error(
            msg=f"The specified path '{args.directory}' is not a directory or does not exist."
        )
        sys.exit(1)

    output_directory: str = args.output or args.directory
    if not os.path.isdir(output_directory):
        os.makedirs(output_directory, exist_ok=True)
        logging.info(msg=f"Created output directory '{output_directory}'")

    jpg_files: list[str] = list(file_generator(args.directory, ".jpg"))
    if not jpg_files:
        logging.error(msg="No .jpg files found in the specified directory.")
        sys.exit(0)

    num_threads: int = (
        args.threads if isinstance(args.threads, int) else os.cpu_count() or 1
    )
    logging.info(msg=f"Using {num_threads} threads for conversion.")

    converter: Converter = Converter(
        output_directory,
        args.retries,
        args.compression,
        args.retry_delay,
        args.dry_run,
        args.improve,
        args.upscale
    )

    # Register signal handlers for clean shutdown
    shutdown_event: threading.Event = threading.Event()
    signal.signal(signal.SIGINT, lambda s, f: shutdown_event.set())
    signal.signal(signal.SIGTERM, lambda s, f: shutdown_event.set())

    start_time: float = time.time()
    success_count: int = 0
    failure_count: int = 0
    task_queue: Queue = Queue()

    try:
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            threading.Thread(
                target=dynamic_thread_adjustment,
                args=(executor, task_queue, shutdown_event),
                daemon=True,
            ).start()

            futures: dict[Future[bool], str] = {executor.submit(converter.convert, file): file for file in jpg_files}
            for future in tqdm(as_completed(futures), total=len(jpg_files), desc="Converting", unit="file"):
                try:
                    result: bool = future.result()
                    task_queue.put(result)
                    if result:
                        success_count += 1
                    else:
                        failure_count += 1
                except Exception as e:
                    logging.error(msg=f"An error occurred: {e}")
                    failure_count += 1
    except KeyboardInterrupt:
        logging.warning("Conversion process interrupted by user.")
        sys.exit(1)

    total_time: float = time.time() - start_time
    logging.info(msg=f"Conversion completed in {total_time:.2f} seconds")
    logging.info(msg=f"Successfully converted {success_count} files")
    logging.info(msg=f"Failed to convert {failure_count} files")


if __name__ == "__main__":
    main()
