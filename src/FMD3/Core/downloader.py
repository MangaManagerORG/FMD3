from zipfile import ZipFile

import FMD3.Core.logging
import asyncio
import logging
import os
from pathlib import Path
from queue import Queue
from ComicInfo import ComicInfo
from threading import Thread
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

from sqlalchemy import exc

from FMD3.Core.FileManagerUtils import make_filename, get_output_folder
from FMD3.Core.database.models import DLDChapters, Series
from FMD3.Core.database.predefined import create_db_chapter
from FMD3.Extensions import IExtension
from FMD3.Models.Chapter import Chapter
from FMD3.Models.MangaInfo import MangaInfo

NUM_THREADS = 3
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


def download_series_chapter(module: IExtension, series, data: MangaInfo, chapter: Chapter) -> DLDChapters:
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
    image_url_list = module.on_get_pages_list(chapter.id)
    series_folder = Path(f"{os.getcwd()}/test_download_lib/{series.save_to or series.title}")
    series_folder.mkdir(exist_ok=True, parents=True)

    cbz_filename = make_filename(chapter, series.title)

    output_file_path = Path(get_output_folder(series_folder), cbz_filename)

    try:
        download_n_pack_pages(cbz_filename, image_url_list)

        append_cinfo(cbz_filename, make_cinfo(data, chapter))
    except:
        os.remove(cbz_filename)
        return None

    return create_db_chapter(chapter, series)







def make_cinfo(data: MangaInfo, chapter: Chapter):
    # Eventually call enrichers here
    cinfo: ComicInfo = data.to_comicinfo_with_chapter_data(chapter)
    return cinfo





def append_cinfo(cbz_path: str, cinfo: ComicInfo)
    with ZipFile(cbz_path, mode="a") as zf:
        zf.writestr("ComicInfo.xml", str(cinfo.to_xml()))


def download_n_pack_pages(cbz_path, images_url_list):
    with ZipFile(cbz_path, mode="w") as zf:
        for i, a in enumerate(images_url_list):
            img_url, image_name = a
            image_name, image_extension = os.path.splitext(image_name)

            new_filename = f"{str(i).zfill(3)}{image_extension}"
            download_image(zf, img_url, new_filename)


def download_missing_chapters_from_series(ext: IExtension, series: Series, data: MangaInfo):
    logger = logging.getLogger(__name__)
    futures = []
    for chapter in data.chapters:
        if chapter_exists(chapter.id):
            logger.info(f"Chapter id {chapter.id}, number {chapter.number} is registered in db. Skipping")
            continue
        futures.append(pool.submit(download_series_chapter, ext, series, data, chapter))
    for future in as_completed(futures):
        result = future.result()

        if isinstance(result, DLDChapters):
            Session.add(result)
    print("")
    pool.shutdown(wait=True)
    Session.commit()


def chapter_exists(chapter_id):
    # return False
    return bool(Session.query(DLDChapters).filter_by(chapter_id=chapter_id).all())


# def download(extension_downloads: list[tuple[IExtension, list[str]]]):
#     # module: IExtension, url):
#     """Here goes the job to be added into the thread pool"""
#     for module, series_list in extension_downloads:
#         pool.submit(download_chapter, module, series)


"""Defining thread pool"""

pool = ThreadPoolExecutor(max_workers=NUM_THREADS)

# """Workflow - TODO"""
# pool.add_task(job,parama_a)
# pool.wait_completion()
