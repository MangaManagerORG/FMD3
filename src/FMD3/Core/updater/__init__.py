import logging
import time

from FMD3.Core import database as db
from FMD3.Core.TaskManager import TaskManager
from FMD3.Core.database import Series
from FMD3.Core.database.predefined import chapter_exists
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
            return False

        output_file_path = make_output_path(series, chapter)

        TaskManager().submit_series_chapter(ext, series.series_id, chapter, output_file_path)


def new_chapters_finder():
    init_time = time.time()
    for source in get_sources_list():
        # get all series in favourites that are from this extension
        s = db.Session()

        series_list: list[db.Series] = s.query(db.Series).filter_by(source_id=source.ID).all()
        for series in series_list:
            last_db_chapter = series.max_chapter_number
            new_chapter_list = source.get_new_chapters(series.series_id, last_db_chapter or -1)
            if not new_chapter_list:
                print("No new chapters found")
                continue
            make_download_task_missing_chapters(source, series, new_chapter_list)

            # print("DONWLOADING NEW CHAPTERS")
    final_time = time.time() - init_time
    print("FINAL:" + str(final_time))