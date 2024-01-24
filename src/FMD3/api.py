import abc

import FMD3
from FMD3.Core import database
from FMD3.Core.database import DLDChapters, Series
from FMD3.Core.updater import create_download_task
from FMD3.Sources import list_sources, get_source


def get_series() -> list[database.Series]:
    return database.Session().query(database.Series).all()


def get_chapters() -> database.DLDChapters:
    return database.Session().query(database.Series).all()



def get_chapters_from_serie_id(series_id):
    return database.Session().query(DLDChapters).filter_by(series_id=series_id).all()

def download_chapters(source: str,series_id: str, chapter_ids: list[str]):
    source = get_source(source)
    chapters = source.get_queried_chapters(series_id,chapter_ids)

    series = database.Session.query(Series).filter_by(series_id=series_id).one_or_none()
    if not series:
        data = source.get_info(series_id)
        try:
            series = Series(series_id=data.id, title=data.title) # todo add missing data
            series.source_id = get_source("MangaDex").ID
            database.Session().add(series)
            database.Session().flush()
            database.Session().commit()
        except:
            # logging.getLogger().error("Error creating series")
            database.Session().rollback()
    create_download_task(source,series,chapters)

def get_loaded_sources():
    return list_sources()


def get_series_for_source(source_id):
    return database.Session().query(database.Series).filter_by(source_id=source_id).all()


def get_chapters_for_series(series_id) -> list[DLDChapters]:
    return database.Session().query(database.Series).filter_by(series_id=series_id).one().chapters
