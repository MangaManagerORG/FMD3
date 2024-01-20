import logging
import os
import urllib.request
from zipfile import ZipFile

from FMD3.Core.database import Session, DLDChapters
from FMD3.Core.downloader.utils import append_cinfo
from FMD3.Sources import ISource

logger = logging.getLogger(__name__)


def download_image(zout, img_url, new_filename):
    """Downloads the image from the url and appends it to the zipfile with the given filename"""
    try:
        logger.info(f"Downloading from '{img_url}'")
        # urllib.request.urlretrieve(img_url, Path(folder,filename))
        url = urllib.request.urlopen(img_url)
        zout.writestr(new_filename, url.read())
    except Exception:
        logger.exception("Exception downloading")


def download_n_pack_pages(cbz_path, images_url_list: list[str]):
    with ZipFile(cbz_path, mode="w") as zf:
        for i, img_url in enumerate(images_url_list,start=1):
            image_name, image_extension = os.path.splitext(img_url)

            new_filename = f"{str(i).zfill(3)}{image_extension}"
            download_image(zf, img_url, new_filename)


def download_series_chapter(module: ISource, series_id, chapter, output_file_path, cinfo):
    """

    Args:
        module:
        series_id:
        chapter:
        output_file_path:
        cinfo:

    Returns:

    """
    image_url_list = module.get_page_urls_for_chapter(chapter.id)
    try:
        download_n_pack_pages(output_file_path, image_url_list)
        append_cinfo(output_file_path, cinfo)
    except Exception:
        logger.exception("Unhandled exception. Cleanin up files")
        os.remove(output_file_path)
        return None
    Session.add(DLDChapters.from_chapter(chapter, series_id))
    Session.commit()
    return True
