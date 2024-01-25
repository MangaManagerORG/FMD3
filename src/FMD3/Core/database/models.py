import enum
from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, String, DateTime, Text, ForeignKey, SmallInteger, func
from sqlalchemy.orm import relationship

from .base import Base
from ...Models.Chapter import Chapter
from ...Models.MangaInfo import MangaInfo


class Series(Base):
    __tablename__ = 'series'

    # id = Column(Integer, autoincrement=True)
    series_id = Column(Text, nullable=False, primary_key=True)
    order = Column(Integer)
    enabled = Column(Boolean)
    source_id = Column(String(255))
    link = Column(String(255))
    title = Column(Text)
    status = Column(SmallInteger)
    currentchapter = Column(Integer)
    save_to = Column(Text)

    dateadded = Column(DateTime, server_default=func.now)
    datelastchecked = Column(DateTime)
    datelastupdated = Column(DateTime)

    chapters = relationship("DLDChapters", backref="series")


class DLDChaptersStatus(enum.Enum):
    NOT_DOWNLOADED = 0
    DOWNLOADED = 1  # Chapter completed
    ADDED_TO_QUEUE = 2  # added to queue. (If program exists these will be loaded first on next scan)
    SKIPPED = 3  # (file existing and apparently correct)
    ERRORED = 4  # Chapter downloads that errored. #Todo: reload them in tasks (maybe on next scan? add retry counter?)


class DLDChapters(Base):
    """Represents a downloaded chapter"""
    __tablename__ = 'DLDChapters'
    # _id = Column(Integer, autoincrement=True)
    chapter_id = Column(String(30), primary_key=True, nullable=False)
    series_id = Column(String(30), ForeignKey("series.series_id"), primary_key=True, nullable=False)

    number = Column(SmallInteger)
    volume = Column(SmallInteger)
    title = Column(Text)
    status = Column(Integer, default=DLDChaptersStatus.NOT_DOWNLOADED.value)
    path = Column(Text)
    downloaded_at = Column(DateTime, server_default=func.now())

    # series = relationship("Series",back_populates="DLDChapters")

    @staticmethod
    def from_chapter(chapter: Chapter, series_id: str):
        ret = DLDChapters()
        ret.chapter_id = chapter.id
        ret.series_id = series_id
        ret.number = chapter.number
        ret.title = chapter.title
        ret.volume = chapter.volume
        return ret
    # series_id = Column(Integer, ForeignKey('series.chapter_id'))
    # series = orm.relationship('Series', backref='dld_chapters')


# Series()
class SeriesCache(Base):
    __tablename__ = 'series_cache'
    series_id = Column(Text, nullable=False, primary_key=True)
    cached_date = Column(DateTime, server_default=func.now())

    title = Column(Text, nullable=False)
    alt_titles = Column(Text)  # Assuming a JSON-serialized list
    description = Column(Text)
    authors = Column(Text)  # Assuming a JSON-serialized list
    artists = Column(Text)  # Assuming a JSON-serialized list
    cover_url = Column(Text)
    genres = Column(Text)  # Assuming a JSON-serialized list
    demographic = Column(Text)
    rating = Column(Text)
    status = Column(Text)

    @property
    def manga_info(self):
        """Return a MangaInfo object from the SeriesCache data."""
        mi = MangaInfo()
        mi.id = self.series_id
        mi.title = self.title
        mi.alt_titles = ",".join(self.alt_titles) if self.alt_titles else []
        mi.description = self.description
        mi.authors = ",".join(self.authors) if self.authors else []
        mi.artists = ",".join(self.artists) if self.artists else []
        mi.cover_url = self.cover_url
        mi.genres = ",".join(self.genres) if self.genres else []
        mi.demographic = self.demographic
        mi.rating = self.rating
        mi.status = self.status
        mi.chapters = []  # Assuming you don't have a direct Chapter relationship in SeriesCache
        return mi

    def update(self, manga_info):
        self.cached_date = datetime.now()

        self.title = manga_info.title
        self.alt_titles = ",".join(manga_info.alt_titles) if manga_info.alt_titles else None
        self.description = manga_info.description
        self.authors = ",".join(manga_info.authors) if manga_info.authors else None
        self.artists = ",".join(manga_info.artists) if manga_info.artists else None
        self.cover_url = manga_info.cover_url
        self.genres = ",".join(manga_info.genres) if manga_info.genres else None
        self.demographic = manga_info.demographic
        self.rating = manga_info.rating
        self.status = manga_info.status
    @classmethod
    def from_manga_info(cls, manga_info):
        """Create a SeriesCache instance from a MangaInfo object."""
        mi = SeriesCache()
        mi.series_id = manga_info.id
        mi.title = manga_info.title
        mi.alt_titles = ",".join(manga_info.alt_titles) if manga_info.alt_titles else None
        mi.description = manga_info.description
        mi.authors = ",".join(manga_info.authors) if manga_info.authors else None
        mi.artists = ",".join(manga_info.artists) if manga_info.artists else None
        mi.cover_url = manga_info.cover_url
        mi.genres = ",".join(manga_info.genres) if manga_info.genres else None
        mi.demographic = manga_info.demographic
        mi.rating = manga_info.rating
        mi.status = manga_info.status
        return mi
