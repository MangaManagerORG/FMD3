import dataclasses

from FMD3.Models.Chapter import Chapter


@dataclasses.dataclass(init=False)
class MangaInfo():
    """Class to store values of a series info"""

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

# a = MangaInfo()
