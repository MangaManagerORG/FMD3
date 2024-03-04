import logging
from typing import Literal, List

from FMD3.extensions.sources import get_source as sup_get_source
from FMD3.api.models.chapters import ChapterResponse, SourceChapterResponse, DownloadChapterForm
from FMD3.core import database as db
from FMD3.core.updater import create_download_task
from FMD3.core.utils import get_series_folder_name
from FMD3.models.chapter import Chapter
from FMD3.models.ddl_chapter_status import DLDChaptersStatus

logging.getLogger()


def get_chapters(series_id) -> List[ChapterResponse]:
    chapters = [
        ChapterResponse(**{
            "chapter_id": chapter.chapter_id,
            "series_id": chapter.series_id,
            "volume": chapter.volume,
            "number": chapter.number,
            "title": chapter.title,
            "status": DLDChaptersStatus(chapter.status),
            "path": chapter.path,
            "added_at": chapter.added_at,
            "downloaded_at": chapter.downloaded_at
        })
        for chapter in db.Session.query(db.DLDChapters).filter_by(series_id=series_id).all()
    ]

    return chapters


def get_source_chapters(source_id, series_id, filter_=None) -> list[ChapterResponse]:
    """
    Returns the chapters from the source. Will only return sources bigger than filter number
    Args:
        source_id:
        series_id:
        filter_:

    Returns:
        Chapters that are of bigger number else empty list

    """
    source = sup_get_source(source_id=source_id)
    if filter_:
        chapters = source.get_new_chapters(series_id, filter_)
    else:
        chapters = source.get_chapters(series_id)

    chapters: list[Chapter]
    return [SourceChapterResponse(**{
        "chapter_id": chapter.chapter_id,
        "volume": chapter.volume,
        "number": chapter.number,
        "title": chapter.title,
        "pages": chapter.pages,
        "scanlator": chapter.scanlator
    })
            for chapter in chapters]


def download_chapters(item:DownloadChapterForm) -> list[Chapter]:
    source = sup_get_source(source_id=item.source_id)
    if item.chapter_ids == "all":
        chapters = source.get_chapters(item.series_id)
    else:
        chapters = source.get_queried_chapters(item.series_id, item.chapter_ids)
    if not chapters:
        return
    series = db.Session.query(db.Series).filter_by(series_id=item.series_id).one_or_none()
    if not series:
        data = source.get_info(item.series_id)
        try:
            series = db.Series(series_id=data.id, title=data.title)  # todo add missing data
            series.enabled = item.enable_series
            series.favourited = item.fav_series
            series.save_to = item.output_path if item.output_path is not None else get_series_folder_name(manga=series.title)
            series.source_id = item.source_id
            db.Session().add(series)
            db.Session().flush()
            db.Session().commit()
        except:
            logging.getLogger().exception("Error creating series")
            db.Session().rollback()
    create_download_task(source, series, chapters, True)
