import os
from enum import StrEnum

from FMD3.Core.settings.models.SettingSection import SettingSection

from FMD3.Core.settings.models.SettingControl import SettingControl as SC, SettingControlType

from FMD3.Core.settings.Keys import *

# class SettingHeading(StrEnum):
#     Main = "Main",
#     WebpConverter = "Webp Converter",
#     ExternalSources = "External Sources",
#     MessageBox = "Message Box"

#

default_settings = [
    SettingSection("General",General,[
        SC(General.LIBRARY_PATH, "Root downloads path",SettingControlType.Text,value=os.getcwd())
    ]),
    SettingSection("SaveTo", SaveTo, [
        SC(SaveTo.DEFAULT_DOWNLOAD_PATH, "Default download path", SettingControlType.Text),
        SC(SaveTo.DEFAULT_DOWNLOAD_FORMAT, "Default download path", SettingControlType.Radio, values=["CBZ"]),
        # ,"PDF","EPUB"])

        SC(SaveTo.SERIES_FOLDER_NAME, "Manga folder name", SettingControlType.Text),
        SC(SaveTo.CHAPTER_NAME, "Chapter name", SettingControlType.Text)
    ]),
    SettingSection("Updates",Updates,[
        SC(Updates.CHECK_NEW_FAV_CHAPTERS_INTERVAL_MINUTES, "interval minutes",SettingControlType.Number,value=1)
    ])
]
