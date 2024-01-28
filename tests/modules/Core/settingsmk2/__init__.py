import unittest
import os
from pathlib import Path
from unittest.mock import patch

import FMD3.Core.settingsmk2
from FMD3.Core.settingsmk2 import Settings, SettingKeys, SettingType, SettingControl


# class TestSettingsInit(unittest.TestCase):
#
#     def setUp(self):
#         self.settings = Settings()
#
#     def tearDown(self):
#         Settings.__class__.__instance = None
#         Settings._settings_dict = {}
#         if Path(Settings._config_file).exists():
#             os.remove(Settings._config_file)
#
#     def test_settings_init_should_create_blank_file(self, *_):
#         self.assertTrue(Path(Settings._config_file).exists())
#
#         self.assertEqual(self.settings._settings_dict, {})

@patch("FMD3.Core.settingsmk2.Settings.save")
class TestSettingsDefaults(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()

    def tearDown(self):
        Settings.__instance = None
        Settings._settings_dict = {}
        if Path(Settings._config_file).exists():
            os.remove(Settings._config_file)

    def test_settings_default_are_created(self, *_):
        class customkeys(SettingKeys):
            test1 = "test1"

        defaults = [
            SettingControl.create(customkeys.test1,
                                  "name",
                                  "tooltip",
                                  None,
                                  "default_value_1",
                                  ["possible_value_1"],
                                  SettingType.Text
                                  )
        ]
        self.settings.load_defaults(defaults)

        self.assertEqual(self.settings.get_control(customkeys.test1).value, "default_value_1")

    def test_settings_default_should_not_override_existing_settings(self, *_):
        class customkeys(SettingKeys):
            test1 = "test1"

        defaults = [
            SettingControl.create(customkeys.test1,
                                  "name",
                                  "tooltip",
                                  None,
                                  "default_value_1",
                                  ["possible_value_1"],
                                  SettingType.Text
                                  )
        ]
        self.settings.load_defaults(defaults)
        value = "definitely not a default value"
        # Asuming a file was read and has different value
        self.settings.set(customkeys.test1, value)

        self.settings.load_defaults(defaults)

        self.assertEqual(self.settings.get_control(customkeys.test1).value, value)
