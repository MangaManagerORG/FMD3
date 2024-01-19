import abc
from typing import final

from FMD3.Core.settings import Settings
from FMD3.Core.database.models import Series
from FMD3.Core.settings.models.SettingSection import SettingSection
from FMD3.Models.Chapter import Chapter
from FMD3.Models.MangaInfo import MangaInfo

SOURCES_SECTIONS_PREFIX = "source_"


class ISource(abc.ABC):
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
    def get_last_chapter(self, serie_id: Series.series_id) -> float:
        ...

    @abc.abstractmethod
    def init_settings(self):
        """
        Method called in extension initialization to load custom settings into main app
        -- Grabs extension settings and loads it to the base setting controller
        :return:
        """

    # Hooks
    # @abc.abstractmethod
    def get_info(self, url) -> MangaInfo:
        """
        Method that retrieves only basic series data.
        Args:
            url:

        Returns:

        """
        ...

    @abc.abstractmethod
    def get_chapters(self, series_id) -> list[Chapter]:
        ...

    @abc.abstractmethod
    def get_page_urls_for_chapter(self, chapter_id) -> list[str]:
        """
        Called when the core requests the list of pages (images url)
        :param chapter_id:
        :return:
        """
        ...

    @staticmethod
    @abc.abstractmethod
    def get_all_series(self) -> list[tuple[str, str]]:
        ...

    def on_get_directory_page_number(self):
        ...

    # @abc.abstractmethod
    def on_login(self):
        ...

    # @abc.abstractmethod
    def on_account_state(self):
        ...
