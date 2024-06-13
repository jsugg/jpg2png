"""
Module for converting .jpg files to .png files with optional improvements
and upscaling.

Classes:
    Converter: Handles the conversion process.
"""

import os
import time
import logging
from PIL import Image, ImageEnhance

logger: logging.Logger = logging.getLogger("jpg2png.converter")


class Converter:
    def __init__(
        self,
        output_directory: str,
        retries: int = 3,
        compression_level: int = 6,
        retry_delay: int = 1,
        dry_run: bool = False,
        improve: bool = False,
        upscale: int = 1,
    ) -> None:
        self.output_directory: str = output_directory
        self.retries: int = retries
        self.compression_level: int = compression_level
        self.retry_delay: int = retry_delay
        self.dry_run: bool = dry_run
        self.improve: bool = improve
        self.upscale: int = upscale

    def convert(self, file_path: str) -> bool:
        """
        Convert a .jpg file to a .png file.

        Args:
            file_path (str): Path to the .jpg file.

        Returns:
            bool: True if conversion is successful, False otherwise.
        """
        png_filename: str = f"{os.path.splitext(os.path.basename(file_path))[0]}.png"
        png_path: str = os.path.join(self.output_directory, png_filename)
        attempt: int = 0

        if self.dry_run:
            logger.info(msg=f"Dry run: would convert {file_path} to {png_path}")
            return True

        while attempt < self.retries:
            try:
                start_time: float = time.time()
                with Image.open(file_path) as img:
                    if self.improve:
                        img = self.improve_image(img)
                    if self.upscale > 1:
                        img = self.upscale_image(img, self.upscale)
                    img.save(
                        png_path, "PNG", compress_level=self.compression_level
                    )
                end_time: float = time.time()
                logger.info(
                    msg=f"Converted {file_path} to {png_path} in {end_time - start_time:.2f} seconds"
                )
                return True
            except (IOError, OSError) as e:
                attempt += 1
                logger.error(
                    msg=f"Attempt {attempt} failed to convert {file_path}: {e}"
                )
                time.sleep(self.retry_delay)
            except Exception as e:
                logger.error(msg=f"Non-recoverable error occurred: {e}")
                break

        logger.error(
            msg=f"Failed to convert {file_path} after {self.retries} attempts"
        )
        return False

    def improve_image(self, img: Image.Image) -> Image.Image:
        """
        Improve the quality of the image.

        Args:
            img (Image.Image): Image to improve.

        Returns:
            Image.Image: Improved image.
        """
        sharpness_enhancer: ImageEnhance.Sharpness = ImageEnhance.Sharpness(img)
        img: Image.Image = sharpness_enhancer.enhance(2.0)  # Sharpen the image
        contrast_enhancer: ImageEnhance.Contrast = ImageEnhance.Contrast(img)
        img = contrast_enhancer.enhance(1.5)  # Enhance contrast
        return img

    def upscale_image(self, img: Image.Image, factor: int) -> Image.Image:
        """
        Upscale the image by a given factor.

        Args:
            img (Image.Image): Image to upscale.
            factor (int): Factor by which to upscale the image.

        Returns:
            Image.Image: Upscaled image.
        """
        width: int
        height: int
        width, height = img.size
        new_size: tuple[int, int] = (width * factor, height * factor)
        return img.resize(new_size, Image.LANCZOS)
