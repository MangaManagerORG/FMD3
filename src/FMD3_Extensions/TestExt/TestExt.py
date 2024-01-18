from FMD3.Core.settings.models.SettingSection import SettingSection
from FMD3.Extensions import IExtension, add_extension


class TestExt(IExtension):

    def init_settings(self):
        self.settings: list[SettingSection] = []

    def on_get_pages_list(self):
        pass

    def on_get_name_and_link(self):
        pass

    def on_get_info(self):
        pass


def load_extension():
    add_extension(TestExt())
