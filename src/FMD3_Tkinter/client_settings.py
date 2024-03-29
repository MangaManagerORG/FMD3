import json
import time
from pathlib import Path

import userpaths

CONFIG_PATH = Path(userpaths.get_local_appdata(), "FMD3", "client_config")
CONFIG_PATH.mkdir(parents=True, exist_ok=True)

_json_file = Path(CONFIG_PATH, "client_settings.json")  # Todo: Change this to a more appropriate location


class Settings:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not Settings.__instance:
            Settings.__instance = object.__new__(cls)
            Settings.__instance._settings_dict = {"host": None}
            Settings._config_file = _json_file
            if not Settings._config_file.exists():
                Settings.__instance.save()
                time.sleep(0.5)
            Settings.__instance.load()
        return Settings.__instance

    def set(self, key, value):
        """
        To be used in the Core namespace to set Core settings. Extensions should use set_value
        Args:
            key:
            value:

        Returns:
        """
        self._settings_dict[key] = value

    def get(self, key):
        """
        To be used in the Core namespace to set Core settings. Extensions should use get_value
        Args:
            key:

        Returns:

        """
        return self._settings_dict[key]

    def save(self):
        with open(self._config_file, "w", encoding='UTF-8') as f:
            json.dump(self._settings_dict, f)

    def load(self):
        with open(self._config_file, "r") as f:
            # print(f.readlines())
            self._settings_dict = json.load(f)
