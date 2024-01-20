import abc
from typing import final

from FMD3.Core.settings import Settings
from FMD3.Core.database.models import Series
from FMD3.Core.settings.models.SettingSection import SettingSection
from FMD3.Models.Chapter import Chapter
from FMD3.Models.MangaInfo import MangaInfo

SOURCES_SECTIONS_PREFIX = "source_"


class IBaseSource(metaclass=abc.ABCMeta):
    ...


class _ChapterMethods(IBaseSource):
    def get_max_chapter(self, series_id: str) -> float:
        """
        Convenience method. uses get_chapters and sorts them
        Args:
            series_id:

        Returns:
        """

        chapters = self.get_chapters(series_id)
        last_chapter = list(filter(lambda x: x.number == max(chapter.number for chapter in chapters),
                                   chapters))
        if last_chapter:
            return last_chapter[0].number

    def get_new_chapters(self, series_id:str , last_chapter_in_db: float) -> list[Chapter]:
        """
        Convenience method. Uses get_chapters and sorts them.
        Gets all the chapters continuing last downloaded
        Args:
            series_id:
            last_chapter_in_db: Last chapter saved as downloaded in the database

        Returns: List of Chapters that have not been downloaded.
        """
        chapters = self.get_chapters(series_id)
        return list(filter(lambda x: x.number > last_chapter_in_db, chapters))

    @abc.abstractmethod
    def get_chapters(self, series_id:str) -> list[Chapter]:
        """
        Gets all the chapters from a series
        Args:
            series_id:

        Returns:

        """


class _SeriesMethods(IBaseSource):
    @staticmethod
    @abc.abstractmethod
    def get_all_series() -> list[tuple[str, str]]:
        """
        Returns all the series available in the source.
        Args:

        Returns:

        """

    @abc.abstractmethod
    def get_info(url) -> MangaInfo:
        """
        Method that retrieves only basic series data.
        Args:
            url:

        Returns:

        """
        ...


class ISource(_SeriesMethods, _ChapterMethods):
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
        return Settings().get(SOURCES_SECTIONS_PREFIX + self.__class__.__name__, setting_key)

    @final
    def set_setting(self, setting_key, value):
        return Settings().set(SOURCES_SECTIONS_PREFIX + self.__class__.__name__, setting_key, value)

    @final
    def __init__(self):
        for source_heading_data in [self.ID, self.NAME, self.ROOT_URL, self.CATEGORY]:
            if source_heading_data is None:
                raise Exception(f"Failed to load source, missing {source_heading_data=} attribute")

        self.settings: list[SettingSection] | None = []
        self.init_settings()
        for section in self.settings:
            for control in section.values:
                Settings().set_default(SOURCES_SECTIONS_PREFIX + section.key, control.key, control.value)
        Settings().save()

    @abc.abstractmethod
    def init_settings(self):
        """
        Method called in extension initialization to load custom settings into main app
        -- Grabs extension settings and loads it to the base setting controller
        :return:
        """

    @abc.abstractmethod
    def get_page_urls_for_chapter(self, chapter_id) -> list[str]:
        """
        Called when the core requests the list of pages (images url)
        :param chapter_id:
        :return:
        """
        ...
