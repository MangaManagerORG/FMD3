from string import Template

from FMD3.Core.settings import Settings
from FMD3.Core.settings.Keys import SaveTo

Settings().set(SaveTo, SaveTo.SERIES_FOLDER_NAME, "manga_name: {manga} author: {author}")


def get_series_folder_name(website=None, manga=None, author=None, artist=None):
    t = Template(Settings().get(SaveTo, SaveTo.SERIES_FOLDER_NAME))
    if not manga:
        raise Exception("Series folder name must have atleast ${MANGA}")
    assert t.is_valid()
    return t.safe_substitute(
        WEBSITE=website,
        MANGA=manga,
        AUTHOR=author,
        ARTIST=artist
    )


def get_chapter_name(website=None, manga=None, chapter=None, author=None, artist=None, numbering=None, volume=None):
    if not chapter and not numbering:
        raise Exception("Chapter folder name must have atleast ${CHAPTER} or ${NUMBERING}")
    t = Template(Settings().get(SaveTo, SaveTo.SERIES_FOLDER_NAME))
    assert t.is_valid()
    return t.safe_substitute(
        WEBSITE=website,
        MANGA=manga,
        CHAPTER=chapter,
        AUTHOR=author,
        ARTIST=artist,
        NUMBERING=numbering,
        VOLUME=volume
        # todo: add volume
    )
