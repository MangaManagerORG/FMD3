import json

from FMD3.Core import database as db
from FMD3.Core.settings import Settings
from FMD3.Core.updater import create_download_task
from FMD3.Models.Chapter import Chapter
from FMD3.Sources import get_source as sup_get_source, get_sources_list


def get_series():
    return [
        {
            "series_id": series.series_id,
            "order": series.order,
            "enabled": series.enabled,
            "source_id": series.source_id,
            "link": series.link,
            "title": series.title,
            "status": series.status,
            "max_chapter": None if not series.chapters else max(series.chapters, key=lambda x: x.number,
                                                                default=0).number,
            "save_to": series.save_to,
            "dateadded": series.dateadded,
            "datelastchecked": series.datelastchecked,
            "datelastupdated": series.datelastupdated,

        }
        for series in db.Session().query(db.Series).all()
    ]


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


def get_series_info(source_id, series_id):
    source = sup_get_source(source_id=source_id)
    series_info = source.get_series_info(series_id)
    if not series_info:
        return {}
    return {
        "id": series_info.id,
        "title": series_info.title,
        "alt_titles": series_info.alt_titles,
        "description": series_info.description,
        "authors": series_info.authors,
        "artists": series_info.artists,
        "cover_url": series_info.cover_url,
        "genres": series_info.genres,
        "demographic": series_info.demographic,
        "rating": series_info.rating,
        "status": series_info.status,
        "chapters": series_info.chapters
    }


def query_series(source_id, series_query):
    source = sup_get_source(source_id=source_id)
    series_list = source.find_series(series_query)
    return [{
        "series_id": series.series_id,
        "title": series.title,
        "cover_url": series.cover_url
    }
        for series in series_list]


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


def download_chapters(source_id: str, series_id: str, chapter_ids: list[str]):
    source = sup_get_source(source_id=source_id)
    chapters = source.get_queried_chapters(series_id, chapter_ids)

    series = db.Session.query(db.Series).filter_by(series_id=series_id).one_or_none()
    if not series:
        data = source.get_info(series_id)
        try:
            series = db.Series(series_id=data.id, title=data.title)  # todo add missing data
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
