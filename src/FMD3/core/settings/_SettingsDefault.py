import os

from . import SettingKeys, SettingControl, SettingType


class Keys(SettingKeys):
    LIBRARY_PATH = "default_downloads_path"
    LIBRARIES_LIST = "libraries_alias_paths_list"
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
    REPLACE_UNICODE = "replace_unicode"  # registered in ui
    REPLACE_UNICODE_WITH = "replace_unicode_with"  # registered in ui
    GENERATE_SERIES_FOLDER = "generate_series_folder"  # registered in ui
    SERIES_FOLDER_NAME = "series_folder_name"  # registered in ui
    REMOVE_MANGA_NAME_FROM_CHAPTER_NAME = "remove_manga_name_from_chapter_name"  # registered in ui
    CHAPTER_NAME = "chapter_name"  # registered in ui
    RENAME_DIGITS_VOLUME = "rename_chapter_digits_volume"
    RENAME_DIGITS_VOLUME_VALUE = "rename_chapter_digits_volume_value"
    RENAME_DIGITS_CHAPTER = "rename_chapter_digits_chapter"
    RENAME_DIGITS_CHAPTER_VALUE = "rename_chapter_digits_chapter_value"

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
        key=Keys.DEFAULT_DOWNLOAD_PATH,
        name="Default download path",
        def_value="",
        type_=SettingType.Text
    ),
    SettingControl.create(
        key=Keys.DEFAULT_DOWNLOAD_FORMAT,
        name="Default download format",
        def_value="",
        type_=SettingType.Radio,
        values=["CBZ"]
    ),
    # RENAMING SECTION
    SettingControl.create(
        key=Keys.REPLACE_UNICODE,
        name="Interval minutes",
        def_value=True,
        type_=SettingType.Bool
    ),
    SettingControl.create(
        key=Keys.REPLACE_UNICODE_WITH,
        name="Interval minutes",
        def_value="_",
        type_=SettingType.Text
    ),
    SettingControl.create(
        key=Keys.GENERATE_SERIES_FOLDER,
        name="Generate folder based on manga's name",
        def_value=True,
        type_=SettingType.Text
    ),
    # generate series folder
    SettingControl.create(
        key=Keys.SERIES_FOLDER_NAME,
        name="Manga folder name",
        def_value="${MANGA}",
        type_=SettingType.Text
    ),
    # remove_manga_name
    SettingControl.create(
        key=Keys.CHAPTER_NAME,
        name="Chapter name",
        def_value="${CHAPTER} ${VOLUME}",
        type_=SettingType.Text
    ),
    SettingControl.create(
        key=Keys.CHECK_NEW_FAV_CHAPTERS_INTERVAL_MINUTES,
        name="Interval minutes",
        def_value=1,
        type_=SettingType.Number
    ),
    SettingControl.create(
        key=Keys.RENAME_DIGITS_CHAPTER,
        name="",
        def_value=True,
        type_=SettingType.Text
    ),
    SettingControl.create(
        key=Keys.RENAME_DIGITS_VOLUME,
        name="",
        def_value=True,
        type_=SettingType.Text
    ),
    SettingControl.create(
        key=Keys.RENAME_DIGITS_VOLUME_VALUE,
        name="",
        def_value=2,
        type_=SettingType.Number
    ),
    SettingControl.create(
        key=Keys.RENAME_DIGITS_CHAPTER_VALUE,
        name="",
        def_value=3,
        type_=SettingType.Number
    ),
    SettingControl.create(
        key=Keys.LIBRARIES_LIST,
        name="Libraries_list",
        def_value=[],
        type_=SettingType.STR_ARRAY
    )

]
