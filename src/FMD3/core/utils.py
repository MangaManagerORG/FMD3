import logging
from pathlib import Path
from string import Template

import pathvalidate

from FMD3 import get_source
from FMD3.models.chapter import Chapter
from FMD3.core.database import Series
from FMD3.core.settings import Keys
from FMD3.core.settings import Settings
from FMD3.errors import TemplateMissingTag


def make_output_path(series: Series, chapter: Chapter):
    """
    Grabs user preferences and sets the output path the cbz will be created at
    Args:
        series:
        chapter:

    Returns:

    """
    # Get filenames and output file
    root_folder = Settings().get(Keys.DEFAULT_DOWNLOAD_PATH)
    # manga_folder_name = get_series_folder_name(manga=series.title)
    manga_folder_name = series.save_to
    cbz_filename = get_chapter_name(manga=series.title,
                                    chapter=chapter.number,
                                    volume=chapter.volume,
                                    website=get_source(source_id=series.source_id).NAME) + ".cbz" # fm.make_filename(chapter, series.title)

    # Create folders
    parent_folder = Path(root_folder, manga_folder_name)
    parent_folder.mkdir(parents=True, exist_ok=True)

    return Path(root_folder, manga_folder_name, cbz_filename)


def cleanup_final_string(string):
    return string.replace("[]", "").replace("{}", "").replace("  ", " ")


def get_series_folder_name(website=None, manga=None, author=None, artist=None):
    user_pref_template = Settings().get(Keys.SERIES_FOLDER_NAME)
    if manga is None:
        raise KeyError("manga attribute cannot be empty")
    if not "${MANGA}" in user_pref_template:
        raise TemplateMissingTag("Series folder template must have atleast ${MANGA}")

    t = Template(user_pref_template)
    assert t.is_valid()
    folder_name = t.safe_substitute(
        WEBSITE=website if website else "",
        MANGA=manga,
        AUTHOR=author if author else "",
        ARTIST=artist if artist else ""
    )
    return pathvalidate.sanitize_filename(cleanup_final_string(folder_name))


def get_chapter_name(website=None, manga=None, chapter=None, author=None, artist=None, volume=None):
    if chapter is None:
        raise KeyError("arguments must include chapter")

    user_pref_template = Settings().get(Keys.CHAPTER_NAME)
    if not "${CHAPTER}" in user_pref_template and not "${NUMBERING}" in user_pref_template:
        raise TemplateMissingTag("Atleast ${CHAPTER} or ${NUMBERING} is required in chapter template")
    if chapter % 1 == 0:
        chapter = int(chapter)
    # raise Exception("Chapter folder name must have atleast ${CHAPTER} or ${NUMBERING}")
    t = Template(user_pref_template)
    assert t.is_valid()
    chapter_name = t.safe_substitute(
        WEBSITE=website if website else "",
        MANGA=manga if manga else "",
        CHAPTER=f"Ch.{str(chapter).zfill(3)}" if chapter else "",
        AUTHOR=author if author else "",
        ARTIST=artist if artist else "",
        NUMBERING=chapter,
        VOLUME=f"Vol.{str(volume).zfill(2)}" if volume else ""
    )
    return cleanup_final_string(chapter_name)
