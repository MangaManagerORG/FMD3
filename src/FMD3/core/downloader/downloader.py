import io
import logging

import requests

from FMD3.models.download_task import DownloadTask

logger = logging.getLogger()


def download_image(session: requests.Session, img_url) -> tuple[str, io.BytesIO]:
    """
    Download image from the given URL synchronously.

    Args:
        session: requests Session.
        img_url: Image URL.

    Returns:
        bytes: Downloaded image data.
    """
    try:
        with session.get(img_url) as response:
            response.raise_for_status()
            logger.debug(f"Downloaded {img_url}")

            # Read the image data into memory
            image_data = io.BytesIO(response.content)

    except Exception:
        logger.exception(f"Exception downloading from '{img_url}'")
        raise

    return img_url, image_data


def download_images_for_chapter(task: DownloadTask) -> DownloadTask:
    for url in task.images_url:
        task.img_bytes_list.append(download_image(task.source.session, url))
    return task


