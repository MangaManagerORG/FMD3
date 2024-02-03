import json
import pathlib

from FMD3.core import database as db
from FMD3.core.settings import Settings, Keys
from FMD3.core.updater import create_download_task
from FMD3.core.utils import get_series_folder_name
from FMD3.models.chapter import Chapter
from FMD3.sources import get_source as sup_get_source, get_sources_list


def get_source(name=None, source_id=None):
    src = sup_get_source(name=name, source_id=source_id)
    source = {}
    source["id"] = src.ID
    source["name"] = src.NAME
    source["root_url"] = src.ROOT_URL
    source["category"] = src.CATEGORY
    source["maxtasklimit"] = src.MaxTaskLimit
    return source


def get_chapters(series_id):
    chapters = [
        {
            "chapter_id": chapter.chapter_id,
            "series_id": chapter.series_id,
            "volume": chapter.volume,
            "number": chapter.number,
            "title": chapter.title,
            "status": db.DLDChaptersStatus(chapter.status).as_name(),
            "path": chapter.path,
            "download_date": chapter.downloaded_at
        }
        for chapter in db.Session.query(db.DLDChapters).filter_by(series_id=series_id).all()
    ]

    return chapters


def get_source_chapters(source_id, series_id, filter: int = None):
    """
    Returns the chapters from the source. Will only return sources bigger than filter number
    Args:
        source_id:
        series_id:
        filter:

    Returns:
        Chapters that are of bigger number else empty list

    """
    source = sup_get_source(source_id=source_id)
    if filter:
        chapters = source.get_new_chapters(series_id, filter)
    else:
        chapters = source.get_chapters(series_id)

    chapters: list[Chapter]
    return [{
        "chapter_id": chapter.chapter_id,
        "volume": chapter.volume,
        "number": chapter.number,
        "title": chapter.title,
        "pages": chapter.pages,
        "scanlator": chapter.scanlator
    }
        for chapter in chapters]


def get_sanitized_download(website=None, manga=None, author=None, artist=None):
    return pathlib.Path(Settings().get(Keys.DEFAULT_DOWNLOAD_PATH),
                        get_series_folder_name(website=website, manga=manga, author=author, artist=artist))


def get_sources():
    return [
        {
            "id": source.ID,
            "name": source.NAME
        }
        for source in get_sources_list()
    ]


def get_cover(source_id, request_url):
    source = sup_get_source(source_id=source_id)
    return source.session.get(request_url)


def download_chapters(source_id: str, series_id: str, chapter_ids: list[str], output_path=None):
    source = sup_get_source(source_id=source_id)
    chapters = source.get_queried_chapters(series_id, chapter_ids)

    series = db.Session.query(db.Series).filter_by(series_id=series_id).one_or_none()
    if not series:
        data = source.get_info(series_id)
        try:
            series = db.Series(series_id=data.id, title=data.title)  # todo add missing data
            series.enabled = True
            series.save_to = output_path if output_path is not None else get_series_folder_name(manga=series.title)
            series.source_id = source_id
            db.Session().add(series)
            db.Session().flush()
            db.Session().commit()
        except:
            # logging.getLogger().error("Error creating series")
            db.Session().rollback()
    create_download_task(source, series, chapters)


def get_settings():
    return Settings().to_json()


def update_settings(new_settings):
    new_set = json.loads(new_settings)
    Settings().update(new_set)


def update_save_to(series_id, new_value):
    if new_value is None:
        return
    db.Session().query(db.Series).filter_by(series_id=series_id).one_or_none().save_to = new_value
    db.Session().commit()
