import os
import logging
import signal
import sys
from typing import Any, Generator

logger: logging.Logger = logging.getLogger("jpg2png.utils")


def configure_logging(log_level: str = "INFO", log_file: str = "error_log.txt") -> None:
    """
    Configures the logging settings for the application.

    Args:
        log_level (str): The log level to set for the logger. Defaults to "INFO".
        log_file (str): The log file path. Defaults to "error_log.txt".

    Returns:
        None
    """
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    formatter: logging.Formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    error_log: logging.FileHandler = logging.FileHandler(log_file)
    error_log.setLevel(logging.ERROR)
    error_log.setFormatter(formatter)
    logger.addHandler(error_log)

    console_handler: logging.StreamHandler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def file_generator(
    directory: str, extension: str
) -> Generator[str, None, None]:
    """
    Generate file paths with the given extension in the specified directory.

    Args:
        directory (str): Path to the directory.
        extension (str): File extension to filter by.

    Yields:
        str: Full path to each file with the given extension.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(extension):
                yield os.path.join(root, file)


def handle_signal(signal: int, frame: Any) -> None:
    """
    Handle termination signals for a clean shutdown.

    Args:
        signal (int): The signal number.
        frame (Any): The current stack frame.

    Returns:
        None
    """
    logger.warning("Termination signal received. Shutting down...")
    sys.exit(1)
