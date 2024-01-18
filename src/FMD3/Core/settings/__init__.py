import configparser
import logging
import os
from pathlib import Path

from .Keys import SectionKeys
from ._SettingsDefault import default_settings
from FMD3.Core.settings.models.SettingSection import SettingSection

logger = logging.getLogger()
SETTING_FILE = "settings.ini"


class Settings:
    """ This is a singleton that holds settings.ini key/values """
    __instance = None
    config_parser = configparser.ConfigParser(interpolation=None)
    _config_file: Path = Path(Path.home(), "MangaManager/" + SETTING_FILE)

    @property
    def config_file(self):
        return Settings._config_file

    def __new__(cls):
        if Settings.__instance is None:
            Settings.__instance = object.__new__(cls)
            # Settings._config_file= os.path.abspath(config_file)

        if len(Settings.__instance.config_parser.sections()) == 0:
            logger.info('Loading Config from: {}'.format(Settings.__instance.config_file))
            Settings.__instance.load()

        return Settings.__instance

    def __init__(self):
        # self.config_file = config_file
        if os.path.exists(self.config_file):
            self.load()
        else:
            if not os.path.exists(SETTING_FILE):
                self.save()
                self.load()
            else:
                self.load(SETTING_FILE)
                self.save()

    def save(self):
        """Save the current settings from memory to disk"""
        with open(self._config_file, 'w') as configfile:
            self.config_parser.write(configfile)

    def load(self, override_settings_from=None):
        """Load the data from file and populate DefaultSettings"""

        self.config_parser.read(override_settings_from or self._config_file)  # migration, change file location

        # Ensure all default settings exists, else add them
        for i, section in enumerate(default_settings):
            if str(section) not in self.config_parser.sections():
                self.config_parser.add_section(str(section))
            for control in default_settings[i].controls:
                if control.key not in self.config_parser[str(section)] or self.config_parser.get(str(section), control.key) == "":
                    self.config_parser.set(str(section), control.key, str(control.value))

        self.save()

    def get(self, section: type[SectionKeys], key):
        """Get a key's value, None if not present"""

        ## The idea is that when requesting settings you can do Settings().get(General,General.LANGUAGE)
        ## Settings will know if the section_name is a subclasss of SectionKey thus returning the get_name value instead of parsing as string
        ## see Keys.py

        if not section or not key:
            raise Exception("Missing either section or key parameter")
        if not isinstance(section,str):
            section = section.__name__.upper()

        if not self.config_parser.has_section(section) or not self.config_parser.has_option(section, key):
            logger.error('Section or Key did not exist in settings: {}.{}'.format(section, key))
            return None
        value = self.config_parser.get(section, key).strip()
        match value.lower():
            case "true":
                return True
            case "false":
                return False
            case _:
                return value

    def set_default(self, section: SectionKeys, key, value):
        """
        Sets a key's value only if it doesn't exist
        :param section: The section
        :param key: The key of the setting
        :param value: The default value of the setting
        :return:
        """
        section = str(section)
        self._create_section(section)
        if key not in self.config_parser[section]:
            self.config_parser.set(str(section), key, str(value))

    def get_default(self, section: SectionKeys, key, default_value):
        """
        Returns default value and creates the key if it doesn't exist
        """
        # section = str(section)
        self.set_default(section, key, default_value)
        return self.get(section, key)

    def set(self, section: type[SectionKeys], key, value):
        """Sets a key's value. Will Save to disk and reload Settings"""
        section = section.__name__.upper()
        self._create_section(section)
        self.config_parser.set(section, key, str(value))
        self.save()
        self.load()

    def _create_section(self, section: str):
        if section not in self.config_parser:
            self.config_parser.add_section(section)

    def _load_test(self):
        Settings._config_file = "test_settings.ini"
        Settings.config_parser = configparser.ConfigParser(interpolation=None)
        self.save()
        self.load()
