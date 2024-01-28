"""
Contains interfaces to configure and integrate sources into the core
"""
import abc
import logging
from typing import final
from datetime import timedelta, datetime
from FMD3.Core.settings import Settings, SettingControl
from FMD3.Core import database as db
from FMD3.Models.SeriesInfo import SeriesInfo

from FMD3.Sources.ISourceMethods import ISourceMethods
from FMD3.Sources.ISourceNet import ISourceNet

SOURCES_SECTIONS_PREFIX = "source_"


class ISource(ISourceMethods, ISourceNet):
    ...
    ID = None
    NAME = None
    Name = None
    ROOT_URL = None
    CATEGORY = None
    # OnGetInfo = None
    MaxTaskLimit = None

    @final
    def get_setting(self, setting_key):
        return Settings().get_value(self.NAME, setting_key)

    @final
    def set_setting(self, setting_key, value):
        return Settings().set_value(self.NAME, setting_key, value)

    @final
    def __init__(self):
        for source_heading_data in [self.ID, self.NAME, self.ROOT_URL, self.CATEGORY]:
            if source_heading_data is None:
                raise Exception(f"Failed to load source, missing {source_heading_data=} attribute")

        self.settings: list[SettingControl] | None = []
        self.init_settings()

        Settings().load_defaults(self.NAME, self.settings)

    @final
    def get_series_info(self, series_id) -> SeriesInfo | None:
        series = db.Session().query(db.SeriesCache).filter_by(series_id=series_id).one_or_none()
        if not series:
            data = self.get_info(series_id)
            if not data:
                return data
            try:
                series = db.SeriesCache.from_manga_info(data)
                db.Session().add(series)
                db.Session().flush()
                db.Session().commit()
                return series.series_info
            except:
                logging.getLogger().exception("Exception introducing cached serie")
                db.Session().rollback()
                return None
        # Check cache date
        else:
            if series.cached_date + timedelta(days=5) < datetime.now():
                # renew cache
                data = self.get_info(series_id)
                series.update(data)
                db.Session().flush()
                db.Session().commit()
        return series.series_info
