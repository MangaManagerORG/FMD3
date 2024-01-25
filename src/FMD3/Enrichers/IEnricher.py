import abc
from typing import final
from ComicInfo import ComicInfo

from FMD3.Models.Chapter import Chapter
from FMD3.Models.SeriesInfo import SeriesInfo


class IEnricher(abc.ABC):
    NAME: str

    @final
    def __init__(self):
        ...

    @abc.abstractmethod
    def process(self, series_data: SeriesInfo, chapters: Chapter, comicinfo: ComicInfo) -> tuple[SeriesInfo, Chapter, ComicInfo]:
        ...
