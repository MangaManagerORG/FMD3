from FMD3.Core.settings.models.SettingControl import SettingControl


class SettingSection:
    """
     A section of config controls. Will render under a group in Settings window
    """

    # pretty_name: str = ''
    # controls: list[SettingControl] = []

    def __init__(self, name, key, controls: list[SettingControl] | None = None):
        if controls is None:
            controls = list()
        self.pretty_name = name
        self.key = key
        self.values = controls

    def get_control(self, key):
        for v in self.controls:
            if v.key == key:
                return v
        return None
