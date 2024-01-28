import json
import logging
from enum import StrEnum, Enum
from pathlib import Path

_json_file = Path("config/" + "settings.json")


class SettingKeys(StrEnum):
    ...


class SettingType(Enum):
    Bool = 0
    Text = 1
    Options = 2
    Number = 3
    Radio = 4


class SettingControl:

    def __init__(self):
        self.key = None
        self.values = None
        self.def_value = None
        self.tooltip = None
        self.type = None
        self.name = None
        self.value = None

    @classmethod
    def create(cls, key: SettingKeys, name, tooltip, value, def_value, values: list[str], type_: SettingType):
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
            "key": self.key,
            "name": self.name,
            "value": self.value,
            "type": self.type.value,
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


class Settings:
    _settings_dict = {}
    __instance = None

    def __new__(cls):
        if Settings.__instance is None:
            Settings.__instance = object.__new__(cls)
            Settings.__instance._settings_dict = {}
            Settings._config_file = Path(_json_file)
            if not Settings._config_file.exists():
                Settings.__instance.save()
            Settings.__instance.load()

        return Settings.__instance

    def add_control(self, control: SettingControl):
        if self._settings_dict.get(control.key.value, None) is None:
            self._settings_dict[control.key.value] = control.to_dict()

    def get_control(self, key: SettingKeys):
        ret = self._settings_dict.get(key.value, None)
        if ret is None:
            raise Exception("control not found")
        else:
            return SettingControl.from_dict(ret)

    def set(self, key: SettingKeys, value):
        if self._settings_dict.get(key.value, None) is None:
            raise Exception("Control not found")
        self._settings_dict[key.value]["value"] = value

    def save(self):
        with open(self._config_file, "w") as f:
            json.dump(self._settings_dict, f)

    def load(self):
        with open(self._config_file, "r") as f:
            self._settings_dict = json.load(f)

    def load_defaults(self, default_controls: list[SettingControl]):
        for control in default_controls:
            if control.key.value not in self._settings_dict:
                self.add_control(control)
