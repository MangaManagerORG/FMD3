import logging
from typing import Literal

from sqlalchemy import desc, asc
from sqlalchemy.sql.base import _NoArg
import jsonpickle

from FMD3 import get_source as sup_get_source
from FMD3.core import database as db
from FMD3.core.database.predefined import get_column_from_str
from FMD3.core.utils import get_series_folder_name as sup_get_series_folder_name
from .sources import get_source_from_url

logger = logging.getLogger(__name__)


def get_fav_series(sort=_NoArg.NO_ARG, order: Literal["asc", "desc"] = "desc", limit=None):
    order = desc if order == "desc" else asc
    q = db.Session().query(db.Series).filter_by(favourited=True)
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
            "max_chapter": -1,
            "save_to": series.save_to,
            "dateadded": series.dateadded,
            "datelastchecked": series.datelastchecked,
            "datelastupdated": series.datelastupdated
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
        "source_id": source.ID,
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
    return series_list


def get_series_folder_name(website=None, manga=None, author=None, artist=None):
    return sup_get_series_folder_name(website, manga, author, artist)


def get_series_from_url(series_url):
    source_id = get_source_from_url(series_url)
    source = sup_get_source(source_id=source_id)
    series_id = source.get_series_id_from_url(series_url)

    return get_series_info(source_id, series_id)


def add_series_favourite(source_id: str, series_id: str, output_path=None):
    source = sup_get_source(source_id=source_id)

    series = db.Session.query(db.Series).filter_by(series_id=series_id).one_or_none()
    if not series:
        data = source.get_info(series_id)
        try:
            series = db.Series(series_id=data.id, title=data.title)  # todo add missing data
            series.enabled = False
            series.favourited = True
            series.save_to = output_path if output_path is not None else get_series_folder_name(manga=series.title)
            series.source_id = source_id
            db.Session().add(series)
            db.Session().flush()
            db.Session().commit()
        except:
            logger.exception("Error creating series")
            db.Session().rollback()
