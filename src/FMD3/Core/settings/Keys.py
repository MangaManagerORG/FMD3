from enum import StrEnum

from FMD3.Core.settings.models.SettingSection import SectionKeys


# The idea is that when requesting settings you can do Settings().get(General,General.LANGUAGE)
# Settings will know if the section_name is a subclasss of SectionKey thus returning the get_name value instead of parsing as string
# See Settings().get()



class General(SectionKeys):
    LIBRARY_PATH = "library_path"
    LANGUAGE = "language"
    ACTION_AFTER_DOWNLOAD = "action_after_download"
    NEW_MANGA_BASED_ON_UPDATE_TIME = "new_manga_based_on_its_update_time"
    MINIMIZE_ON_START = "minimize_on_start"
    MINIMIZE_TO_TRAY = "minimize_to_tray"
    ONLY_ONE_FMD_INSTANCE = "only_one_md_instance"
    DELETE_COMPLETED_TASKS_ON_CLOSE = "only_one_md_instance"
    VACUUM_DB_ON_EXIT = "vacuum_db_onexit"


class SaveTo(SectionKeys):
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

class Updates(SectionKeys):
    AUTO_CHECK_VERSION = "auto_check_version"
    CHECK_NEW_FAV_CHAPTERS = "check_new_fav_chapters"
    CHECK_NEW_FAV_CHAPTERS_ON_INTERVAL = "check_new_fav_chapters_on_interval"
    CHECK_NEW_FAV_CHAPTERS_INTERVAL_MINUTES = "check_new_fav_chapters_interval_minutes"
