import queue
from zipfile import ZipFile

import logging
import os
from pathlib import Path
from ComicInfo import ComicInfo
import urllib.request


from FMD3.Core.database.models import DLDChapters
from FMD3.Sources.ISource import ISource
from FMD3.Models.Chapter import Chapter
from FMD3.Models.MangaInfo import MangaInfo

NUM_THREADS = 10
DL_FOLDER = "test_download_lib"
from FMD3.Core.database.Session import Session

logger = logging.getLogger(__name__)


def download_image(zout, img_url, new_filename):
    """Downloads the image from the url and appends it to the zipfile with the given filename"""
    try:
        logging.getLogger(__name__).info(f"Downloading from '{img_url}'")
        # urllib.request.urlretrieve(img_url, Path(folder,filename))
        url = urllib.request.urlopen(img_url)
        zout.writestr(new_filename, url.read())
    except Exception:
        logging.getLogger(__name__).exception("Exception downloading")


def append_cinfo(cbz_path: Path | str, cinfo: ComicInfo):
    with ZipFile(cbz_path, mode="a") as zf:
        zf.writestr("ComicInfo.xml", str(cinfo.to_xml()))


def download_n_pack_pages(cbz_path, images_url_list):
    with ZipFile(cbz_path, mode="w") as zf:
        for i, a in enumerate(images_url_list):
            img_url, image_name = a
            image_name, image_extension = os.path.splitext(image_name)

            new_filename = f"{str(i).zfill(3)}{image_extension}"
            download_image(zf, img_url, new_filename)


def download_series_chapter(module: ISource, series_id, chapter, output_file_path, cinfo):
    """
    Assigns zipfile filename from series data
    Makes cinfo
    Download pages (images from url)
    Appends comicinfo

    :param module:
    :param series:
    :param data:
    :param chapter:
    :return:
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


def make_cinfo(data: MangaInfo, chapter: Chapter):
    # Eventually call enrichers here
    cinfo: ComicInfo = data.to_comicinfo_with_chapter_data(chapter)
    return cinfo
