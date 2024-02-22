"""
Contains interfaces to configure and integrate sources into the core
"""
from abc import abstractmethod
import logging
from typing import final
from datetime import timedelta, datetime
from requests_ratelimiter import LimiterSession

from FMD3.core.settings import Settings, SettingControl
from FMD3.core import database as db
from FMD3.models.chapter import Chapter
from FMD3.models.series_info import SeriesInfo
from FMD3.extensions.sources.SearchResult import SearchResult

SOURCES_SECTIONS_PREFIX = "source_"


class ISource:
    ...
    ID = None
    NAME = None
    ROOT_URL = None
    CATEGORY = None
    # OnGetInfo = None
    VERSION = None
    MAX_REQUESTS_PER_SECOND = 10

    _has_updates = False  # Becomes true once the updater has been called if new version avaialble
    _session = None

    @final
    def get_setting(self, setting_key):
        return Settings().get_value(self.NAME, setting_key,extension="sources")

    @final
    def set_setting(self, setting_key, value):
        return Settings().set_value(self.NAME, setting_key, value, extension="sources")

    @final
    def __init__(self):
        for source_heading_data in [self.ID, self.NAME, self.ROOT_URL, self.CATEGORY]:
            if source_heading_data is None:
                raise Exception(f"Failed to load source, missing {source_heading_data=} attribute")

        self.settings: list[SettingControl] | None = []
        self.init_settings()

        Settings().load_defaults(self.NAME, self.settings,extension="sources")

    @property
    def session(self):
        if self._session is None:
            self._session = self.create_session()
        return self._session

    @staticmethod
    def create_session():
        """
        Override this method to configure the session and connection settings more specifically.
        """
        return LimiterSession(per_second=5)

    @abstractmethod
    def is_url_from_source(self, url) -> bool:
        """
        Method called passing a url. Mostly to fetch a source from a given url
        :param url:
        :return:
        """
    @abstractmethod
    def get_series_id_from_url(self,url) -> str:
        ...
    @final
    def get_series_info(self, series_id) -> tuple[SeriesInfo | None, None|str]:
        saved_series = db.Session.query(db.Series).filter_by(series_id=series_id).one_or_none()
        save_to = None
        if saved_series:
            save_to = saved_series.save_to

        series = db.Session().query(db.SeriesCache).filter_by(series_id=series_id).one_or_none()
        if not series:
            data = self.get_info(series_id)
            if not data:
                return data, None
            try:
                series = db.SeriesCache.from_manga_info(data)
                db.Session().add(series)
                db.Session().flush()
                db.Session().commit()
                return series.series_info, save_to
            except:
                logging.getLogger().exception("Exception introducing cached serie")
                db.Session().rollback()
                return None, None
        # Check cache date
        else:
            if series.cached_date + timedelta(days=5) < datetime.now():
                # renew cache
                data = self.get_info(series_id)
                series.update(data)
                db.Session().flush()
                db.Session().commit()

        return series.series_info, save_to

    #
    # Source methods
    #

    def get_max_chapter(self, series_id: str, chapter_list: list[Chapter] | None = None) -> float:
        """
        Convenience method. uses get_chapters and sorts them
        Args:
            chapter_list:
            series_id:

        Returns:
        """
        if chapter_list:
            chapters = chapter_list
        else:
            chapters = self.get_chapters(series_id)
        last_chapter = list(filter(lambda x: x.number == max(chapter.number for chapter in chapters),
                                   chapters))
        if last_chapter:
            return last_chapter[0].number

    def get_new_chapters(self, series_id: str, last_chapter: float) -> list[Chapter]:
        """
        Convenience method. Uses get_chapters and sorts them.
        Gets all the chapters continuing last downloaded
        Args:
            series_id:
            last_chapter_in_db: Last chapter saved as downloaded in the database

        Returns: List of Chapters that have not been downloaded.
        """
        chapters = self.get_chapters(series_id)
        return list(filter(lambda x: x.number > last_chapter, chapters))

    @abstractmethod
    def get_chapters(self, series_id: str) -> list[Chapter]:
        """
        Gets all the chapters from a series
        Args:
            series_id:

        Returns:

        """

    def get_queried_chapters(self, series_id, chapters_ids: list[str]):
        return list(filter(lambda x: x.chapter_id in chapters_ids, self.get_chapters(series_id)))

    # @staticmethod
    # @abstractmethod
    # async def get_all_series() -> list[tuple[str, str]]:
    #     """
    #     Returns all the series available in the source.
    #     Args:
    #
    #     Returns:
    #
    #     """

    @abstractmethod
    def get_info(self, url) -> SeriesInfo:
        """
        Method that retrieves only basic series data.
        Args:
            url:

        Returns:

        """
        ...

    @abstractmethod
    def get_page_urls_for_chapter(self, chapter_id) -> list[str]:
        """
        Called when the core requests the list of pages (images url)
        :param chapter_id:
        :return:
        """
        ...

    @abstractmethod
    def find_series(self, query: str) -> list[SearchResult]:
        ...

    @abstractmethod
    def init_settings(self):
        """
        Method called in extension initialization to load custom settings into main app
        -- Grabs extension settings and loads it to the base setting controller
        :return:
        """
    @abstractmethod
    def is_url_from_source(self, url) -> bool:
        """
        Method called passing a url. Mostly to fetch a source from a given url
        :param url:
        :return:
        """

