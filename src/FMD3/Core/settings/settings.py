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
            Settings.__instance.load_defaults("Core", default_settings)

        return Settings.__instance

    def check_section_or_create(self, section):
        if self._settings_dict.get(section, None) is None:
            self._settings_dict[section] = {}

    def add_control(self, section, control: SettingControl):
        self.check_section_or_create(section)
        if self._settings_dict[section].get(control.key.value, None) is None:
            self._settings_dict[section][control.key.value] = control.to_dict()

    def check_key(self, section, key):
        if self._settings_dict[section].get(key.value, None) is None:
            raise Exception(f"Setting key not found '{section}.{key}'")

    def check_section(self, section):
        if self._settings_dict.get(section, None) is None:
            raise Exception(f"Setting section not found '{section}'")

    def set_value(self, section: str, key: SettingKeys, value):
        self.check_section_or_create(section)
        self._settings_dict[section][key.value]["value"] = value

    def get_value(self, section, key):
        self.check_section(section)
        self.check_key(section, key)

        return self._settings_dict[section][key.value].get("value",
                                                           self._settings_dict[key.value].get("def_value", None))

    def set(self, key: SettingKeys, value):
        """
        To be used in the Core namespace to set Core settings. Extensions should use set_value
        Args:
            key:
            value:

        Returns:
        """
        self.set_value("Core", key, value)

    def get(self, key: SettingKeys):
        """
        To be used in the Core namespace to set Core settings. Extensions should use get_value
        Args:
            key:

        Returns:

        """
        return self.get_value("Core", key)

    def save(self):
        with open(self._config_file, "w") as f:
            json.dump(self._settings_dict, f)

    def load(self):
        with open(self._config_file, "r") as f:
            self._settings_dict = json.load(f)

    def load_defaults(self, section: str, default_controls: list[SettingControl]):
        for control in default_controls:
            if control.key.value not in self._settings_dict:
                self.add_control(section, control)
        self.save()

    def update(self, new_dict):
        for key in new_dict:
            if key in self._settings_dict:
                self._settings_dict[key]["value"] = new_dict[key]["value"]
        self.save()

    def to_json(self):
        return json.dumps(self._settings_dict)
