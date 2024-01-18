import abc
from enum import Enum, StrEnum
from typing import Callable


class SettingControlType(Enum):
    Bool = 0,
    Text = 1,
    Options = 2,
    Number = 3,
    Radio = 4


class SettingControl(abc.ABC):
    key: str = ''
    name: str = ''
    tooltip: str | None = ''
    control_type: SettingControlType
    value = ''
    """
    Only applicable for SettingControlTypes [Options,Radio] 
    """
    values: list = []
    # Used to run validations on the control
    validate: Callable[[str], str] = None
    # Used to format the value before saving to persistence layer
    format_value: Callable[[str], str] = None

    def __init__(self, key, name, control_type, value='', values=None, tooltip='', validate=None, format_value=None):
        if values is None:
            values = []
        if isinstance(key,StrEnum):
            key = key.value
        self.key = key
        self.name = name
        self.control_type: SettingControlType = control_type
        self.value = value
        self.values = values or []
        self.tooltip = tooltip
        self.validate = validate
        self.format_value = format_value

        if value == '' and type is SettingControlType.Bool:
            self.value = False

    def set_values(self, values):
        if self.control_type is not SettingControlType.Options:
            return
        self.values = values
