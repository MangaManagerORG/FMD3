from enum import StrEnum

from FMD3.Core.settings.models.SettingControl import SettingControl, SettingControlType


class Keys(StrEnum):
    SelectedLanguage = "en"

    # LastDelay = "lastDelay"

    """Delay (s) between requests"""
    MDEX_DELAY = "mdex_delay"  #

    REMOVE_TITLE = "opttitle"

    DATA_SAVER = "luadatasaver"

controls = [

    SettingControl(Keys.SelectedLanguage.value, "Selected Language",SettingControlType.Text, "en"),
    SettingControl(Keys.MDEX_DELAY, "Delay (s) between requests", SettingControlType.Number),
    SettingControl(Keys.REMOVE_TITLE,"Remove title from chapter",SettingControlType.Bool),
    SettingControl(Keys.DATA_SAVER,"Use data saver", SettingControlType.Bool)
]
