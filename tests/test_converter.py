import unittest
from unittest.mock import patch, MagicMock
import os
import tempfile
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from jpg2png.converter import Converter
from jpg2png.utils import file_generator


class TestJpgToPngConverter(unittest.TestCase):
    """
    A test suite for verifying the correct conversion of JPG images to PNG format.

    This class contains unit tests for the `Converter` class, ensuring that
    JPG images are properly converted to PNG format according to the expected
    behavior and requirements.
    """

    def setUp(self) -> None:
        """
        Set up the test environment by creating a temporary directory and writing a test file.

        This method is called before each test case is executed. It creates a temporary directory
        using the `tempfile.TemporaryDirectory` class and writes a test file named "test.jpg" with
        the content "fake jpg content" inside the temporary directory.

        Parameters:
            self (TestJpgToPngConverter): The instance of the test class.

        Returns:
            None
        """
        # Create a temporary directory
        self.test_dir: tempfile.TemporaryDirectory = (
            tempfile.TemporaryDirectory()
        )
        self.test_file: str = os.path.join(self.test_dir.name, "test.jpg")
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("fake jpg content")

    def tearDown(self) -> None:
        """
        Clean up the temporary directory.

        This method is called after each test case is executed. It cleans up the temporary directory
        created during the test by calling the `cleanup()` method of the `tempfile.TemporaryDirectory`
        object.

        Parameters:
            self (TestJpgToPngConverter): The instance of the test class.

        Returns:
            None
        """
        self.test_dir.cleanup()

    def test_file_generator(self) -> None:
        """
        Test the `file_generator` function to ensure it correctly finds and returns a list of file paths
        with the extension ".jpg" within the specified directory.

        This test case creates a temporary directory and writes a test file named "test.jpg" with the content
        "fake jpg content" inside the temporary directory. It then calls the `file_generator` function with the
        temporary directory path and the ".jpg" extension. The function returns a generator that yields the file
        paths with the specified extension.

        The test asserts that the length of the returned list is equal to 1 and that the file path at index 0
        matches the test file path.

        Parameters:
            self (TestJpgToPngConverter): The instance of the test class.

        Returns:
            None
        """
        files: list[str] = list(file_generator(self.test_dir.name, ".jpg"))
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0], self.test_file)

    @patch("jpg2png.converter.Image.open")
    def test_convert_jpg_to_png(self, mock_open: MagicMock) -> None:
        """
        Test the `convert` method of the `Converter` class to ensure it correctly converts a JPG image to PNG.

        This test case mocks the `Image.open` method to simulate the opening of a JPG image file.
        It then creates an instance of the `Converter` class with the specified directory and `dry_run` set to `False`.
        The `convert` method is called with the test file path, and the result is checked to ensure it is `True`.
        Finally, it asserts that the `save` method of the mocked image object is called once.

        Parameters:
            self (TestJpgToPngConverter): The instance of the test class.
            mock_open (MagicMock): The mocked `Image.open` method.

        Returns:
            None
        """
        mock_image: MagicMock = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_image

        converter: Converter = Converter(self.test_dir.name, dry_run=False)
        result: bool = converter.convert(self.test_file)

        self.assertTrue(result)
        mock_image.save.assert_called_once()

    def test_dry_run(self) -> None:
        """
        Test the dry run mode of the Converter class.

        This test case creates an instance of the Converter class with the specified directory
        and dry_run set to True.
        It then calls the convert method with the test file path and checks if the result is True.

        Parameters:
            self (TestJpgToPngConverter): The instance of the test class.

        Returns:
            None
        """
        converter: Converter = Converter(self.test_dir.name, dry_run=True)
        result: bool = converter.convert(self.test_file)
        self.assertTrue(result)

    @patch(
        "jpg2png.converter.Image.open",
        side_effect=OSError("Cannot open file"),
    )
    def test_convert_with_retry(self, mock_open: MagicMock) -> None:
        """
        Test the retry mechanism of the `Converter` class.

        This test case mocks the `Image.open` method to simulate the opening of a file that raises an `OSError`.
        It creates an instance of the `Converter` class with the specified directory, retries set to 2,
        and retry delay set to 1.
        It then calls the `convert` method with the test file path and checks if the result is `False`.
        Finally, it asserts that the `call_count` of the mocked `Image.open` method is equal to 2.

        Parameters:
            self (TestConverter): The instance of the test class.

        Returns:
            None
        """
        converter: Converter = Converter(
            self.test_dir.name, retries=2, retry_delay=1
        )
        result: bool = converter.convert(self.test_file)

        self.assertFalse(result)
        self.assertEqual(mock_open.call_count, 2)

    @patch(
        "jpg2png.converter.Image.open",
        side_effect=Exception("Non-recoverable error"),
    )
    def test_convert_non_recoverable_error(self, mock_open: MagicMock) -> None:
        """
        Test the handling of non-recoverable errors in the `Converter` class.

        This test case mocks the `Image.open` method to simulate a non-recoverable error.
        It creates an instance of the `Converter` class with the specified directory,
        retries set to 2, and retry delay set to 1.
        It then calls the `convert` method with the test file path and checks if the result is `False`.
        Finally, it asserts that the `call_count` of the mocked `Image.open` method is equal to 1.

        Parameters:
            self (TestConverter): The instance of the test class.
            mock_open (MagicMock): The mocked `Image.open` method.

        Returns:
            None
        """
        converter: Converter = Converter(
            self.test_dir.name, retries=2, retry_delay=1
        )
        result: bool = converter.convert(self.test_file)

        self.assertFalse(result)
        self.assertEqual(mock_open.call_count, 1)


if __name__ == "__main__":
    unittest.main()
