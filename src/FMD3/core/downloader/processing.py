import io
import logging
import os
from io import BytesIO
from zipfile import ZipFile

from PIL import Image, ImageStat

from FMD3.models.download_task import DownloadTask
from FMD3.models.ddl_chapter_status import DLDChaptersStatus
logger = logging.getLogger(__name__)
max_dimensions = (16383, 16383)

is_convert = True


def convert_image(image_data:io.BytesIO) -> io.BytesIO:
    """
    Convert image data to webp format.

    Args:
        image_raw_data: Raw image data.

    Returns:
        bytes: Converted image data.
    """
    try:
        logger.info("Converting image")
        image = Image.open(image_data)
        # Check if resizing is needed
        is_grayscale = image.mode in ('L', 'LA') or all(
            min(channel) == max(channel) for channel in ImageStat.Stat(image).extrema
        )
        # Choose resampling method based on image content
        if is_grayscale:
            # For grayscale images (e.g., manga pages)
            resample_method = Image.NEAREST  # or Image.BILINEAR
        else:
            # For colored images (e.g., covers)
            resample_method = Image.BICUBIC  # or Image.LANCZOS
        # Check if resizing is needed
        if any(dim > max_dim for dim, max_dim in zip(image.size, max_dimensions)):
            # Resize the image with the chosen resampling method
            image.thumbnail(max_dimensions, resample=resample_method)
        converted_image_data = BytesIO()
        image.save(converted_image_data, format="webp")
        converted_image_data.seek(0)
        return converted_image_data
    except Exception as e:
        logger.error(f"Exception converting image: {e}")
        raise


def convert_and_zip(task: DownloadTask):
    try:
        with ZipFile(task.output_path, "w") as zout:
            for i, image_data in enumerate(task.img_bytes_list):
                image_url, image_bytes_io = image_data
                image_filename = os.path.splitext(os.path.basename(image_url))
                assert image_filename[1] != ''
                new_filename = f"{i:03}.{image_filename[1]}"
                if is_convert:
                    try:
                        image_bytes = convert_image(image_bytes_io).getvalue()
                        new_filename = f"{i:03}.webp"
                    except Exception:
                        logger.exception("Exception converting image. Using not converted_file")
                        image_bytes = image_bytes_io.getvalue()
                else:
                    image_bytes = image_bytes_io.getvalue()

                try:
                    zout.writestr(new_filename, image_bytes)
                    task.status = DLDChaptersStatus.DOWNLOADED
                except Exception:
                    logger.exception("Exception writing to zipfile")
                    task.status = DLDChaptersStatus.ERRORED
                    break

    except Exception as e:
        print(e)
        logger.exception("Unhandled exception converting image bytes")
        task.status = DLDChaptersStatus.ERRORED
    finally:
        # clean so bytes won't be pickled
        task.img_bytes_list = None
    return task
