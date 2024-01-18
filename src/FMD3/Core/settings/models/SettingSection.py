from enum import StrEnum

from FMD3.Core.settings.models.SettingControl import SettingControl


class SectionKeys(StrEnum):
    """Abstract class to check"""

    def __str__(self):
        self.__class__.__name__.upper()


class SettingSection:
    """
     A section of config controls. Will render under a group in Settings window
    """

    # pretty_name: str = ''
    # controls: list[SettingControl] = []

    def __init__(self, name: str, key: type[SectionKeys], controls: list[SettingControl] | None = None):
        if controls is None:
            controls = list()
        self.controls = controls
        self.pretty_name = name
        self.key = key
        self.values = controls

    def __str__(self):
        return self.key.__name__.upper()

    def get_control(self, key: type[SectionKeys] | str):

        for v in self.controls:
            if v.key == key:
                return v
        return None
