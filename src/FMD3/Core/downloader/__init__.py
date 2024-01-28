import asyncio
import logging
import os
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

import aiohttp
from PIL import Image, ImageStat

from FMD3.Core.database.models import DLDChaptersStatus
from FMD3.Core.downloader.utils import append_cinfo
from FMD3.Models.Chapter import Chapter
from FMD3.Sources import ISource

logger = logging.getLogger(__name__)
max_dimensions = (16383, 16383)


async def convert_image(image_raw_data):
    """
    Convert image data to webp format.

    Args:
        image_raw_data: Raw image data.

    Returns:
        bytes: Converted image data.
    """
    try:
        logger.info("Converting image")
        image = Image.open(BytesIO(image_raw_data))
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
        return converted_image_data.getvalue()
    except Exception as e:
        logger.error(f"Exception converting image: {e}")
        raise


async def download_image(session, img_url):
    """
    Download image from the given URL asynchronously.

    Args:
        session: aiohttp ClientSession.
        img_url: Image URL.

    Returns:
        bytes: Downloaded image data.
    """
    try:
        async with session.get(img_url) as response:
            response.raise_for_status()
            logger.debug(f"Downloaded {img_url}")
            return await response.read()
    except Exception:
        logger.exception(f"Exception downloading from '{img_url}'")
        raise


async def download_and_convert(session, img_url, index, is_convert):
    """
    Download an image, optionally convert it, and save it to a ZIP file.

    Args:
        session (aiohttp.ClientSession): Aiohttp client session for making HTTP requests.
        cbz_path (str): The path to the output ZIP file.
        img_url (str): URL of the image to download and save.
        index (int): Index of the image in the sequence.
        is_convert (bool): If True, convert the image to webp format. Default is True.

    Returns:
        tuple: A tuple containing the new filename and image data.

    Raises:
        Exception: If any exception occurs during the process.
    """
    try:
        # Download the image
        image_data = await download_image(session, img_url)

        # Optionally convert the image
        if is_convert:
            image_data = await convert_image(image_data)
            new_filename = f"{index:03}.webp"
        else:
            new_filename, _ = os.path.splitext(os.path.basename(img_url))

        return new_filename, image_data

    except Exception as e:
        logger.error(f"Exception processing '{img_url}': {e}")
        raise


async def download_n_pack_pages(cbz_path, images_url_list, is_convert=True):
    """
    Download and pack a list of images into a ZIP file.

    Args:
        cbz_path: Path to the output ZIP file.
        images_url_list: List of image URLs.
        is_convert: Whether to convert images to webp format.

    Raises:
        Exception: If any exception occurs during the process.
    """
    tasks = []
    async with aiohttp.ClientSession() as session:
        for i, img_url in enumerate(images_url_list, start=1):
            tasks.append(download_and_convert(session, img_url, i, is_convert))

        # Use gather to run tasks concurrently and obtain their results
        return await asyncio.gather(*tasks)


def cleanup_files(path):
    try:
        os.remove(path)
    except:
        logger.exception("Faile to cleanup files")


def analyze_archive(output_file_path, series_id, chapter:Chapter) -> bool:
    """
        Analyzes an archive file to determine if it exists and has the correct number of files.

        Parameters:
        - output_file_path (str): The path to the archive file to be analyzed.
        - series_id (str): The identifier of the series.
        - chapter (Chapter): The Chapter object representing the chapter information.

        Returns:
        - bool: True if the file exists and has the correct number of files, indicating that it has already been downloaded;
                False otherwise, indicating that the file needs to be processed.

        The function checks if the specified archive file exists. If it exists, it reads the contents of the archive to
        determine the number of image files (".webp", ".jpg", ".png") and chapter information files (".xml"). If the count
        matches the expected number of pages in the chapter plus one (for the chapter information file), it logs a warning
        message indicating that the file is already downloaded and returns True. Otherwise, it returns False, indicating
        that the file needs to be processed further.
        """
    if Path(output_file_path).exists():

        with ZipFile(output_file_path, "r") as zf:
            n_images_and_cinfo = len([file for file in zf.namelist() if
                                      os.path.splitext(file)[1].lower() in [".webp", ".jpg", ".png", ".xml"]])
            if n_images_and_cinfo == chapter.pages + 1:
                logger.warning(
                    f"File '{output_file_path}' - series '{series_id}' chapter number '{chapter.number}' chapter id '{chapter.chapter_id}' is apparently already downloaded. Skipping with status 4")
                return True
    return False


def download_series_chapter(source: ISource, series_id, chapter: Chapter, output_file_path, cinfo) -> tuple[
    str, str, DLDChaptersStatus]:
    """
    Download a chapter of a series.

    Args:
        source: Source module.
        series_id: ID of the series.
        chapter: Chapter object.
        output_file_path: Output path for the ZIP file.
        cinfo: ComicInfo object.

    Returns:
        bool: True if the download was successful, False otherwise.
    """

    try:
        # Check file is not downloaded:
        if analyze_archive(output_file_path, series_id, chapter):
            return series_id, chapter.chapter_id, DLDChaptersStatus.SKIPPED

        image_url_list = source.get_page_urls_for_chapter(chapter.chapter_id)
        try:
            tasks = asyncio.run(download_n_pack_pages(output_file_path, image_url_list))
            with ZipFile(output_file_path, "w") as zout:
                for filename, data in tasks:
                    zout.writestr(filename, data)

            append_cinfo(output_file_path, cinfo)
        except Exception as e:
            logger.exception(f"Unhandled exception. Cleaning up files: {e}")
            cleanup_files(output_file_path)
            return series_id, chapter.chapter_id, DLDChaptersStatus.ERRORED

    except Exception as e:
        logger.exception(f"Unhandled exception. Cleaning up files: {e}")
        cleanup_files(output_file_path)

        return series_id, chapter.chapter_id, DLDChaptersStatus.ERRORED
    return series_id, chapter.chapter_id, DLDChaptersStatus.DOWNLOADED
