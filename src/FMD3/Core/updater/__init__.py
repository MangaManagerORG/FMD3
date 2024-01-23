import logging
import time

from FMD3.Core import database as db
from FMD3.Core.TaskManager import TaskManager
from FMD3.Core.database import Series
from FMD3.Core.database.predefined import chapter_exists, max_chapter_number
from FMD3.Core.utils import make_output_path
from FMD3.Models.Chapter import Chapter
from FMD3.Sources import get_sources_list, ISource

logger = logging.getLogger(__name__)


def download_missing_chapters(source: ISource, series: Series, chapters: list[Chapter]):
    """
    Downloads and saves a list of chapters from a given source to the user's preferred location,
    only if the chapters do not already exist in the database.

    Parameters:
        source (ISource): The source object for downloading the chapters.
        series (Series): The series to which the chapters belong.
        chapters (list[Chapter]): The list of chapters to be downloaded.

    Returns:
        bool: False if any of the chapters already exist in the database.
    """
    for chapter in chapters:
        cinfo = source.get_info(series.series_id).to_comicinfo_with_chapter_data(chapter)
        output_file_path = make_output_path(series, chapter)

        TaskManager().submit_series_chapter(source, series.series_id, chapter, output_file_path, cinfo)


def new_chapters_finder():
    """
       Initiates the process of finding and downloading new chapters for all series in the user's favorites.

       This function iterates through all sources, retrieves series from the user's favorites for each source,
       and identifies new chapters to download. It then calls the make_download_task_missing_chapters function
       to download the new chapters.

       Returns:
           None
       """
    logging.getLogger(__name__).debug("Initiating chapter finder")
    init_time = time.time()
    for source in get_sources_list():
        # get all series in favourites that are from this extension
        s = db.Session()
        logger.debug(f"Found source: {source.NAME}")
        series_list: list[db.Series] = s.query(db.Series).filter_by(source_id=source.ID).all()
        for series in series_list:
            logger.debug(f"Found series: {series.title}")
            last_db_chapter = max_chapter_number(series.series_id)
            new_chapter_list = source.get_new_chapters(series.series_id, last_db_chapter or -1)
            if not new_chapter_list:
                print("No new chapters found")
                continue

            download_missing_chapters(source, series, new_chapter_list)

            # print("DONWLOADING NEW CHAPTERS")
    final_time = time.time() - init_time
    print("FINAL:" + str(final_time))
