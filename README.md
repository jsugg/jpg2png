# jpg2png Converter

This is a Python tool to convert JPG images to PNG format, with optional features to improve image quality and upscale the image resolution.

## Features

- Convert JPG images to PNG format.
- Improve image quality using the `--improve` flag.
- Upscale image resolution using the `--upscale` flag with a specified factor.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/jsugg/jpg2png.git
    ```
2. Navigate to the project directory:
    ```sh
    cd jpg2png
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

Run the script with the required directory path and optional flags:
```sh
python scripts/main.py <directory> [--output <output_directory>] [--threads <num_threads>] [--retries <num_retries>] [--compression <compression_level>] [--log-level <log_level>] [--retry-delay <retry_delay>] [--dry-run] [--improve] [--upscale <factor>]
```

Example:
```sh
python scripts/main.py /path/to/jpg/files --output /path/to/output --improve --upscale 2
```

## Arguments

- `directory`: Path to the directory containing .jpg files.
- `--output`: Path to the directory to save .png files (default: same as input directory).
- `--threads`: Number of threads to use for conversion (default: auto-detect).
- `--retries`: Number of retries for conversion in case of failure (default: 3).
- `--compression`: Compression level for PNG output (0-9, default: 6).
- `--log-level`: Logging level (default: INFO).
- `--retry-delay`: Delay between retries in seconds (default: 1).
- `--dry-run`: Simulate the conversion process without performing any conversions.
- `--improve`: Flag to improve the image quality as much as possible.
- `--upscale`: Upscale factor for the image resolution (default: 1, meaning no upscaling).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
