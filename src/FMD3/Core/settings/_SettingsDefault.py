import os

from . import SettingKeys, SettingControl, SettingType


class Keys(SettingKeys):

    LIBRARY_PATH = "library_path"
    LANGUAGE = "language"
    ACTION_AFTER_DOWNLOAD = "action_after_download"
    NEW_MANGA_BASED_ON_UPDATE_TIME = "new_manga_based_on_its_update_time"
    MINIMIZE_ON_START = "minimize_on_start"
    MINIMIZE_TO_TRAY = "minimize_to_tray"
    ONLY_ONE_FMD_INSTANCE = "only_one_md_instance"
    DELETE_COMPLETED_TASKS_ON_CLOSE = "only_one_md_instance"
    VACUUM_DB_ON_EXIT = "vacuum_db_onexit"

    # class SaveTo(SectionKeys):
    DEFAULT_DOWNLOAD_PATH = "default_download_path"
    DEFAULT_DOWNLOAD_FORMAT = "default_format"
    PDF_QUALITY_LEVEL = "PDF_QUALITY_LEVEL"
    # Todo: add missing keys

    # Renaming section
    REPLACE_UNICODE_WITH = "replace_unicode_with"
    GENERATE_SERIES_FOLDER = "generate_series_folder"
    SERIES_FOLDER_NAME = "series_folder_name"
    REMOVE_MANGA_NAME_FROM_CHAPTER_NAME = "remove_manga_name_from_chapter_name"
    CHAPTER_NAME = "chapter_name"

    # class Updates(SectionKeys):
    AUTO_CHECK_VERSION = "auto_check_version"
    CHECK_NEW_FAV_CHAPTERS = "check_new_fav_chapters"
    CHECK_NEW_FAV_CHAPTERS_ON_INTERVAL = "check_new_fav_chapters_on_interval"
    CHECK_NEW_FAV_CHAPTERS_INTERVAL_MINUTES = "check_new_fav_chapters_interval_minutes"


default_settings = [

    SettingControl.create(
        key=Keys.LIBRARY_PATH,
        name="Root downloads path",
        def_value="",
        type_=SettingType.Text
    ),
    SettingControl.create(
        key=        Keys.DEFAULT_DOWNLOAD_PATH,
        name=       "Default download path",
        def_value=  "",
        type_=      SettingType.Text
    ),
    SettingControl.create(
        key=        Keys.DEFAULT_DOWNLOAD_FORMAT,
        name=       "Default download format",
        def_value=  "",
        type_=      SettingType.Radio,
        values=     ["CBZ"]
    ),
    SettingControl.create(
        key=        Keys.SERIES_FOLDER_NAME,
        name=       "Manga folder name",
        def_value=      "${MANGA}",
        type_=      SettingType.Text
    ),
    SettingControl.create(
        key=        Keys.CHAPTER_NAME,
        name=       "Chapter name",
        def_value=  "${CHAPTER}",
        type_=      SettingType.Text
    ),
    SettingControl.create(
        key=        Keys.CHECK_NEW_FAV_CHAPTERS_INTERVAL_MINUTES,
        name=       "Interval minutes",
        def_value=  1,
        type_=      SettingType.Number
    )
]
