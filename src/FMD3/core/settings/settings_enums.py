from enum import StrEnum, Enum


class SettingKeys(StrEnum):
    ...


class SettingType(Enum):
    Bool = 0
    Text = 1
    Options = 2
    Number = 3
    Radio = 4
    STR_ARRAY = 5