from typing import Literal

from sqlalchemy import desc, asc
from sqlalchemy.sql.base import _NoArg

from FMD3 import get_source as sup_get_source
from FMD3.core import database as db
from FMD3.core.database.predefined import get_column_from_str
from FMD3.core.utils import get_series_folder_name as sup_get_series_folder_name


def get_series(sort=_NoArg.NO_ARG, order: Literal["asc", "desc"] = "desc", limit=None):
    order = desc if order == "desc" else asc
    q = db.Session().query(db.Series)
    if sort != _NoArg.NO_ARG:
        q = q.order_by(order(get_column_from_str("series", sort)))
    if limit:
        q = q.limit(limit)

    return [
        {
            "series_id": series.series_id,
            "enabled": series.enabled,
            "source_id": series.source_id,
            "title": series.title,
            "status": series.status,
            "max_chapter": None if not series.chapters else max(series.chapters, key=lambda x: x.number,
                                                                default=0).number,
            "save_to": series.save_to,
            "dateadded": series.dateadded,
            "datelastchecked": series.datelastchecked,
            "datelastupdated": series.datelastupdated,

        }
        for series in q.all()
    ]


def get_series_info(source_id, series_id):
    source = sup_get_source(source_id=source_id)
    series_info, save_to = source.get_series_info(series_id)
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
        "chapters": series_info.chapters,
        "save_to": save_to
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


def get_series_folder_name(website=None, manga=None, author=None, artist=None):
    return sup_get_series_folder_name(website, manga, author, artist)


def get_cover(source_id, request_url):
    source = sup_get_source(source_id=source_id)
    return source.session.get(request_url)
