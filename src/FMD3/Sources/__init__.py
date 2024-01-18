import abc
from typing import final

from FMD3.Core.settings import Settings

from FMD3.Core.settings.models.SettingSection import SettingSection
from FMD3.Models.MangaInfo import MangaInfo

"""Module with methods related with extensions"""

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
        for source_heading_data in [self.ID, self.NAME,self.ROOT_URL,self.CATEGORY]:
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

    # Hooks
    @abc.abstractmethod
    def on_get_info(self, url) -> MangaInfo:
        ...

    @abc.abstractmethod
    def on_get_pages_list(self, chapter_id) -> list[str]:
        """
        Called when the core requests the list of pages (images url)
        :param chapter_id:
        :return:
        """
        ...

    @abc.abstractmethod
    def on_get_name_and_link(self):
        ...

    def on_get_directory_page_number(self):
        ...

    # @abc.abstractmethod
    def on_login(self):
        ...

    # @abc.abstractmethod
    def on_account_state(self):
        ...


extesion_factory: list[ISource] = []


@abc.abstractmethod
def load_extension(extension: ISource):
    ...
@abc.abstractmethod
def load_source(source: ISource):
    ...

def get_extension(name) -> ISource:
    for ext in extesion_factory:
        if ext.__class__.__name__ == name:
            return ext

def get_extension_list() -> list[ISource]:
    return extesion_factory
def list_extension() -> list[str]:
    return [ext.__class__.__name__ for ext in extesion_factory]


def add_extension(extension: ISource):
    # extension.init_settings()
    extesion_factory.append(extension)
