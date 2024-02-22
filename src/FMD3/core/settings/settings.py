import json
import time
from pathlib import Path

from ._SettingsDefault import default_settings
from ...constants import SETTING_FILE_PATH

from .settings_enums import SettingKeys
from .setting_control import SettingControl


class Settings:
    _settings_dict = {}
    __instance = None

    def get_setting_dict_or_extension(self,extension):
        return self._settings_dict if extension is None else self._settings_dict[extension]

    def __new__(cls):
        if Settings.__instance is None:
            Settings.__instance = object.__new__(cls)
            Settings.__instance._settings_dict = {}
            Settings._config_file = Path(SETTING_FILE_PATH)
            if not Settings._config_file.exists():
                Settings.__instance.save()
            time.sleep(0.5)
            Settings.__instance.load()
            Settings.__instance.load_defaults("Core", default_settings)
            Settings.__instance.save()

        return Settings.__instance

    def check_section_or_create(self, section, extension=None):
        d = self._settings_dict if extension is None else self._settings_dict[extension]
        if d.get(section, None) is None:
            (self._settings_dict if extension is None else self._settings_dict[extension])[section] = {}

    def add_control(self, section, control: SettingControl, extension=None):
        self.check_section_or_create(section,extension)
        if self.get_setting_dict_or_extension(extension)[section].get(control.key.value, None) is None:
            (self._settings_dict if extension is None else self._settings_dict[extension])[section][control.key.value] = control.to_dict()

    def check_key(self, section, key, extension=None):
        if not isinstance(key, str):
            key = key.value
        if self.get_setting_dict_or_extension(extension)[section].get(key,
                                                                                                       None) is None:
            raise Exception(f"Setting key not found {extension} '{section}.{key}'")

    def check_section(self, section):
        if self._settings_dict.get(section, None) is None:
            raise Exception(f"Setting section not found '{section}'")

    def set_value(self, section: str, key: SettingKeys, value, extension=None):
        self.check_section_or_create(section, extension)
        (self._settings_dict[section] if extension is None else self._settings_dict[extension][section])[key.value]["value"] = value

    def get_value(self, section, key, extension=None):
        if self.get_setting_dict_or_extension(extension).get(section, None) is None:
            self.check_key(section, key, extension)
        return self.get_setting_dict_or_extension(extension)[section][
            key.value].get("value",
                           self._settings_dict[section][key.value].get("def_value", None))

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
        with open(self._config_file, "w", encoding='UTF-8') as f:
            json.dump(self._settings_dict, f)

    def load(self):
        with open(self._config_file, "r") as f:
            # print(f.readlines())
            self._settings_dict = json.load(f)

    def load_defaults(self, section: str, default_controls: list[SettingControl], extension=None):
        for control in default_controls:
            if control.key.value not in self.get_setting_dict_or_extension(extension):
                self.add_control(section, control, extension)

    def update(self, new_dict):
        self._settings_dict = new_dict
        self.save()

    def to_json(self):
        return json.dumps(self._settings_dict)
