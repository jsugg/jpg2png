import argparse


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.

    Returns:
        Namespace: Parsed arguments.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Convert all .jpg files in a directory to .png files."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="Path to the directory containing .jpg files",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Path to the directory to save .png files (default: same as input directory)",
    )
    parser.add_argument(
        "--threads",
        type=int,
        help="Number of threads to use for conversion (default: auto-detect)",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=3,
        help="Number of retries for conversion in case of failure (default: 3)",
    )
    parser.add_argument(
        "--compression",
        type=int,
        default=6,
        help="Compression level for PNG output (0-9, default: 6)",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        help="Logging level (default: INFO)",
    )
    parser.add_argument(
        "--retry-delay",
        type=int,
        default=1,
        help="Delay between retries in seconds (default: 1)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the conversion process without performing any conversions",
    )
    parser.add_argument(
        "--improve",
        action="store_true",
        help="Flag to improve the image quality as much as possible",
    )
    parser.add_argument(
        "--upscale",
        type=int,
        default=1,
        help="Upscale factor for the image resolution (default: 1, meaning no upscaling)",
    )

    return parser.parse_args()
