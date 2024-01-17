import abc
from typing import final

from FMD3.Core.settings import Settings

from FMD3.Core.settings.models.SettingSection import SettingSection

"""Module with methods related with extensions"""


EXTENSIONS_SECTIONS_PREFIX = "extension_"


class IExtension(abc.ABC):
    ...
    extension_name = None

    @final
    def get_setting(self, setting_key):
        return Settings().get(EXTENSIONS_SECTIONS_PREFIX + self.__class__.__name__, setting_key)

    @final
    def set_setting(self, setting_key, value):
        return Settings().set(EXTENSIONS_SECTIONS_PREFIX + self.__class__.__name__, setting_key, value)

    @final
    def __init__(self):
        self.settings: list[SettingSection] | None = []
        self.init_settings()
        for section in self.settings:
            for control in section.values:
                Settings().set_default(EXTENSIONS_SECTIONS_PREFIX + section.key, control.key, control.value)
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
    def on_get_info(self):
        ...

    @abc.abstractmethod
    def on_get_page_number(self, url) -> tuple[str, str]:
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


extesion_factory: list[IExtension] = []


@abc.abstractmethod
def load_extension(extension: IExtension):
    ...

def get_extension(name) -> IExtension:
    for ext in extesion_factory:
        if ext.__class__.__name__ == name:
            return ext
def list_extension() -> str:
    return [ext.__class__.__name__ for ext in extesion_factory]
def add_extension(extension: IExtension):
    # extension.init_settings()
    extesion_factory.append(extension)

