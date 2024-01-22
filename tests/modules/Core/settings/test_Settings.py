import io
import os.path
import tempfile
import unittest


from FMD3.Core.settings import Settings

from FMD3.Core.settings import Keys

@unittest.skip("Outdated")
class SettingsTest(unittest.TestCase):

    def setUp(self):
        with tempfile.NamedTemporaryFile("w",delete=False) as tmp_conf:
            Settings.__instance = None
            Settings._config_file = tmp_conf.name
            Settings()
    def tearDown(self):

        Settings.__instance = None
        if os.path.exists(Settings._config_file):
            os.remove(Settings._config_file)
        Settings._config_file = None
        if os.path.exists('settings.ini'):
            print('Cleaning up created settings.ini')
            os.remove('settings.ini')

    @unittest.skip("Outdated")
    def test_default_settings(self):
        """
        Test that deffault settings are set correctly
        Returns:
        """

    @unittest.skip("Outdated")
    def test_Settings_will_create_if_nothing_on_disk(self):
        s = Settings()
        self.assertTrue(os.path.exists(s.config_file))

    @unittest.skip("Outdated")
    def test_Settings_will_set_values(self):
        s = Settings()
        s.set(Keys.General, Keys.General.LIBRARY_PATH, 'test_dir')
        self.assertEqual(s.get(Keys.General, Keys.General.LIBRARY_PATH), 'test_dir')

    @unittest.skip("Outdated")
    def test_Settings_will_write_default_tag_if_not_exists(self):
        s = Settings()
        self.assertNotEqual(s.get(SettingHeading.ExternalSources, 'default_metadata_source'), '')




if __name__ == '__main__':
    unittest.main()
