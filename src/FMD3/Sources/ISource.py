"""
Contains interfaces to configure and integrate sources into the core
"""
import abc
from typing import final

from FMD3.Core.settings import Settings
from FMD3.Core.settings.models.SettingSection import SettingSection

from FMD3.Sources.ISourceMethods import ISourceMethods
from FMD3.Sources.ISourceNet import ISourceNet

SOURCES_SECTIONS_PREFIX = "source_"



class ISource(ISourceMethods,ISourceNet):
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

