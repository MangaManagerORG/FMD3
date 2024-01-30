from .settings_enums import SettingKeys, SettingType


class SettingControl:

    def __init__(self):
        self.key:SettingKeys = None
        self.name:str = None
        self.def_value:str = None
        self.type:SettingType = None
        self.tooltip: str | None = None
        self.values: list[str] | None = None
        self.value: str | None = None

    @classmethod
    def create(cls,
               key: SettingKeys,
               name,
               def_value,
               type_: SettingType,
               tooltip: str | None = None,
               values: list[str] = None,
               value: str | None = None):
        ret = cls()
        ret.key = key
        ret.name = name
        ret.value = value or def_value
        ret.tooltip = tooltip
        ret.def_value = def_value
        ret.values = values
        ret.type = type_
        return ret

    def to_dict(self):
        return {
            "key": self.key.value,
            "name": self.name,
            "value": self.value,
            "type": None if self.type is None else self.type.value,
            "tooltip": self.tooltip,
            "def_value": self.def_value,
            "values": self.values
        }

    @classmethod
    def from_dict(cls, dict_):
        ret = cls()
        ret.key = dict_["key"]
        ret.name = dict_["name"]
        ret.value = dict_["value"]
        ret.type = dict_["type"]
        ret.tooltip = dict_["tooltip"]
        ret.def_value = dict_["def_value"]
        ret.values = dict_["values"]
        return ret
