from enum import StrEnum

from FMD3.Core.settings import SettingKeys, SettingControl, SettingType


class Keys(SettingKeys):
    SelectedLanguage = "en"

    # LastDelay = "lastDelay"

    """Delay (s) between requests"""
    MDEX_DELAY = "mdex_delay"  #

    REMOVE_TITLE = "opttitle"

    DATA_SAVER = "luadatasaver"


controls = [

    SettingControl.create(
        key=Keys.SelectedLanguage,
        name="Selected Language",
        def_value="en",
        type_=SettingType.Text
    ),

    SettingControl.create(
        key=Keys.MDEX_DELAY,
        name="Delay (s) between requests",
        def_value=0,
        type_=SettingType.Number
    ),
    SettingControl.create(
        key=Keys.REMOVE_TITLE,
        name="Remove title from chapter",
        def_value=False,
        type_=SettingType.Bool,
    ),
    SettingControl.create(
        key=Keys.DATA_SAVER,
        name="Use data saver",
        def_value=False,
        type_=SettingType.Bool
    )
]
