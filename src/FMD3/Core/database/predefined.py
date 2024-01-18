from FMD3.Core.database import DLDChapters
from FMD3.Models.Chapter import Chapter


def create_db_chapter(chapter: Chapter, series_id):
    ret = DLDChapters()
    ret.chapter_id = chapter.id
    ret.series_id = series_id
    ret.number = chapter.number
    ret.title = chapter.title
    ret.volume = chapter.volume
    return ret