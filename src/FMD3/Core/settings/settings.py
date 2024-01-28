import json
from pathlib import Path

from ._SettingsDefault import default_settings

_json_file = Path("config/" + "settings.json")

from .settings_enums import SettingKeys
from .setting_control import SettingControl


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
            Settings.__instance.load_defaults(default_settings)

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

    def get(self, key: SettingKeys):
        if self._settings_dict.get(key.value, None) is None:
            raise Exception("Control not found")
        return self._settings_dict[key.value].get("value", self._settings_dict[key.value].get("def_value", None))

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
        self.save()

    def update(self, new_dict):
        for key in new_dict:
            if key in self._settings_dict:
                self._settings_dict[key]["value"] = new_dict[key]["value"]
        self.save()
    def to_json(self):
        return json.dumps(self._settings_dict)
