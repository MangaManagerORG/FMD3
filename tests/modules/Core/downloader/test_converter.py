# import asyncio
# import unittest
# from io import BytesIO
# from unittest.mock import patch, MagicMock
#
# from PIL import Image
#
#
# from FMD3.core.downloader import convert_image
#
#
# class TestImageConverter(unittest.TestCase):
#     def test_convert_image(self):
#         # Mock the Image.open method to return a mock image
#         with patch("FMD3.core.downloader.Image.open") as mock_image_open:
#             # Create a red image for testing
#             red_image = Image.new("RGB", (100, 100), "red")
#
#             # Convert the red image to raw bytes
#             red_image_data = BytesIO()
#             red_image.save(red_image_data, format="JPEG")
#             red_image_data.seek(0)
#
#             # Create a mock image
#             mock_image = MagicMock()
#             mock_image.size = (100, 100)  # Set the image size
#             mock_image.mode = "RGB"  # Set the image mode
#             mock_image.thumbnail.return_value = None  # Mock the thumbnail method
#
#             # Attach the mock image to the mock_image_open method
#             mock_image_open.return_value = mock_image
#
#             # Mock the BytesIO class to capture the converted image data
#             with patch("FMD3.core.downloader.BytesIO") as mock_bytes_io:
#                 # Create a mock BytesIO instance
#                 mock_bytes_io_instance = MagicMock()
#
#                 # Mock the save method of the image to capture the converted image data
#                 mock_image.save.return_value = None
#                 mock_image.save.side_effect = lambda buffer, format: mock_bytes_io_instance.write(buffer.getvalue())
#
#                 # Call the convert_image function with the red image data
#                 result = asyncio.run(convert_image(red_image_data.getvalue()))
#
#                 # Check that the Image.open method is called with the correct arguments
#                 mock_image_open.assert_called_once_with(BytesIO(red_image_data.getvalue()))
#
#                 # Check that the thumbnail method is called with the correct arguments
#                 mock_image.thumbnail.assert_called_once_with((100, 100), resample=Image.NEAREST)
#
#                 # Check that the BytesIO instance is used to capture the converted image data
#                 mock_bytes_io.assert_called_once()
#
#                 # Check that the save method is called with the correct arguments
#                 mock_image.save.assert_called_once_with(mock_bytes_io_instance, format="webp")
#
#                 # Check that the result matches the converted image data captured by BytesIO
#                 self.assertEqual(result, mock_bytes_io_instance.getvalue())
#
