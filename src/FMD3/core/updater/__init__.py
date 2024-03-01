import logging
import time
from datetime import timedelta, datetime

from sqlalchemy import and_, or_

from FMD3.core.TaskManager import TaskManager
from FMD3.core.database import Series, DLDChapters, Session, SeriesCache
from FMD3.core.database.models import SeriesStatus
from FMD3.models.ddl_chapter_status import DLDChaptersStatus
from FMD3.core.database.predefined import max_chapter_number
from FMD3.core.utils import make_output_path
from FMD3.models.chapter import Chapter
from FMD3.extensions.sources import get_sources_list, ISource, get_source_by_id
from FMD3.models.series_info import SeriesInfoStatus

logger = logging.getLogger(__name__)


def create_download_task(source: ISource, series: Series, chapters: list[Chapter], is_user_task=False):
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
    series_info = Session().query(SeriesCache).filter_by(series_id=series.series_id).one_or_none()
    if not series_info:
        series_info = source.get_info(series.series_id)
        sc = SeriesCache.from_manga_info(series_info)
        Session().add(sc)
        Session().commit()
    else:
        logger.info("Using cache for series-info")
        series_info = series_info.series_info

    for chapter in chapters:
        cinfo = series_info.to_comicinfo_with_chapter_data(chapter)
        output_file_path = make_output_path(series, chapter)
        # output_file_path = series.save_to
        # todo: get outputfile path from db series
        TaskManager().submit_series_chapter(source, series.series_id, chapter, output_file_path, cinfo,
                                            manual_download=is_user_task)


def scan_hanging_tasks():
    logger.debug("Starting hanging tasks")
    sources_series_group = {}

    # Query the database for relevant chapters
    for chapterDlD in Session.query(DLDChapters).filter(
        or_(
            and_(
                DLDChapters.status == DLDChaptersStatus.ADDED_TO_QUEUE_SCANNER,
                DLDChapters.added_at + timedelta(hours=3) < datetime.now()
            ),
            and_(
                DLDChapters.status == DLDChaptersStatus.ADDED_TO_QUEUE_USER,
                # DLDChapters.added_at + timedelta(hours=3) < datetime.now()
            )
        )
    ).all():
        source_id = chapterDlD.series.source_id
        series_id = chapterDlD.series_id

        # Populate the sources_series_group dictionary
        if source_id not in sources_series_group:
            sources_series_group[source_id] = {}

        if series_id not in sources_series_group[source_id]:
            sources_series_group[source_id][series_id] = []

        sources_series_group[source_id][series_id].append(chapterDlD)

    # Iterate over the grouped data
    for source_id, series_dict in sources_series_group.items():
        source = get_source_by_id(source_id)

        for series_id, chapters_list in series_dict.items():
            # Fetch new chapters from the source
            new_chapter_list = source.get_queried_chapters(series_id, [chapter.chapter_id for chapter in chapters_list])

            # If there are new chapters, download them
            if new_chapter_list:
                series = chapters_list[0].series
                create_download_task(source, series, new_chapter_list)
        # TODO: testing


def __no_new_chapters():
    """
    Unittest callback when no more chapters to download
    :return:
    """


def scan_new_chapters():
    logging.getLogger(__name__).debug("Initiating chapter finder")
    init_time = time.time()
    for source in get_sources_list():
        # get all series in favourites that are from this extension
        s = Session()
        logger.debug(f"Found source: {source.NAME}")
        series_list: list[Series] = s.query(Series).filter_by(source_id=source.ID, favourited=True,
                                                              enabled=True).filter(Series.status != SeriesStatus.FINISHED_AND_DOWNLOADED).all()
        for series in series_list:
            if series.datelastchecked:
                if series.datelastchecked + timedelta(hours=23) > datetime.now():
                    logger.debug(f"Skipping chapter check for '{series.title}' (checked less than 24 hours ago)")
                    continue

            last_db_chapter = max_chapter_number(series.series_id)
            new_chapter_list = source.get_new_chapters(series.series_id, last_db_chapter or -1)
            if source.get_max_chapter(series.series_id, new_chapter_list) == last_db_chapter:

                series_info = source.get_series_info(series.series_id)
                if series_info:
                    if series_info[0].status == SeriesInfoStatus.COMPLETED:
                        series.status = SeriesStatus.FINISHED
                logger.debug(f"Marking series '{series.title}' as fully downloaded (source max chapter is the same as "
                             f"last chapter in db and series is marked as complete)")
                series.datelastchecked = datetime.now()
                s.commit()
                continue

            series.datelastchecked = datetime.now()
            s.commit()

            create_download_task(source, series, new_chapter_list)

            # print("DONWLOADING NEW CHAPTERS")
    final_time = time.time() - init_time
    print("FINAL:" + str(final_time))


def new_chapters_finder():
    """
       Initiates the process of finding and downloading new chapters for all series in the user's favorites.

       This function iterates through all sources, retrieves series from the user's favorites for each source,
       and identifies new chapters to download. It then calls the make_download_task_missing_chapters function
       to download the new chapters.

       Returns:
           None
       """
    scan_hanging_tasks()
    scan_new_chapters()
