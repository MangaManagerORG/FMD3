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





def make_download_task_missing_chapters(ext: ISource, series: Series, chapter_list: list[Chapter]):
    """
            Downloads a single chapter from a remote source and saves it to the user preferences' location.

            Parameters:
                ext (ISource): The source object for downloading the chapter.
                series (Series): The series to which the chapter belongs.
                chapter_list (Chapter): The chapters to be downloaded.

            Returns:
                bool: `False` if the chapter exists in db.
            """
    # futures = []
    for chapter in chapter_list:

        if chapter_exists(series.series_id, chapter.id):
            logger.info(f"Chapter id {chapter.id}, number {chapter.number} is registered in db. Skipping")
            continue
        cinfo = ext.get_info(series.series_id).to_comicinfo_with_chapter_data(chapter)
        output_file_path = make_output_path(series, chapter)
        logger.info(f"Adding download task for {series.title} . Ch.{chapter.number}")
        TaskManager().submit_series_chapter(ext, series.series_id, chapter, output_file_path,cinfo)

def new_chapters_finder():
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

            make_download_task_missing_chapters(source, series, new_chapter_list)

            # print("DONWLOADING NEW CHAPTERS")
    final_time = time.time() - init_time
    print("FINAL:" + str(final_time))