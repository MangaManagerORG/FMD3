import dataclasses
from ComicInfo import ComicInfo
from FMD3.models.chapter import Chapter


@dataclasses.dataclass(init=False)
class SeriesInfo:
    """Class to store values of a series info"""
    id: str

    title: str
    alt_titles: list
    description: str
    authors: list[str]
    artists: list[str]
    cover_url: str
    genres: list[str]
    demographic: str
    rating: str
    status: str
    chapters: list[Chapter]
    def __init__(self):
        self.title: str = None
        self.alt_titles: list = None
        self.description: str = None
        self.authors: list[str] = None
        self.artists: list[str] = None
        self.cover_url: str = None
        self.genres: list[str] = None
        self.demographic: str = None
        self.rating: str = None
        self.status: str = None
        self.chapters: list[Chapter] = None

    def to_comicinfo(self) -> ComicInfo:
        c = ComicInfo()
        c.series = self.title
        c.summary = self.description
        if self.artists:
            c.cover_artist = ",".join(self.artists)
        if  self.authors:
            c.writer = ",".join(self.authors)
        if self.genres:
            c.genre = ",".join([genre for genre in self.genres if genre is not None])
        return c

    def to_comicinfo_with_chapter_data(self, chapter: Chapter):
        c = self.to_comicinfo()
        c.volume = chapter.volume
        c.number = chapter.number
        c.title = chapter.title
        c.scan_information = c.scan_information
        return c

