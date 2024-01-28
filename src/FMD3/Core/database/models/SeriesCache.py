from datetime import datetime

from sqlalchemy import Column, Text, DateTime, func

from FMD3.Core.database import Base
from FMD3.Models.SeriesInfo import SeriesInfo


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
    def series_info(self):
        """Return a SeriesInfo object from the SeriesCache data."""
        mi = SeriesInfo()
        mi.id = self.series_id
        mi.title = self.title
        if self.alt_titles:
            mi.alt_titles = self.alt_titles.split(",")
        mi.description = self.description
        mi.authors = self.authors.split(",")
        if self.artists:
            mi.artists = self.artists.split(",")

        mi.cover_url = self.cover_url
        if self.genres:
            mi.genres = self.genres.split(",")
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
        self.authors = ",".join(manga_info.authors or []) if manga_info.authors else None
        self.artists = ",".join(manga_info.artists or []) if manga_info.artists else None
        self.cover_url = manga_info.cover_url
        self.genres = ",".join(manga_info.genres or []) if manga_info.genres else None
        self.demographic = manga_info.demographic
        self.rating = manga_info.rating
        self.status = manga_info.status

    @classmethod
    def from_manga_info(cls, manga_info):
        """Create a SeriesCache instance from a SeriesInfo object."""
        mi = SeriesCache()
        mi.series_id = manga_info.id
        mi.title = manga_info.title
        mi.alt_titles = ",".join(manga_info.alt_titles) if manga_info.alt_titles else None
        mi.description = manga_info.description
        mi.authors = ",".join(manga_info.authors or []) if manga_info.authors else None
        mi.artists = ",".join(manga_info.artists or []) if manga_info.artists else None
        mi.cover_url = manga_info.cover_url
        mi.genres = ",".join(manga_info.genres or []) if manga_info.genres else None
        mi.demographic = manga_info.demographic
        mi.rating = manga_info.rating
        mi.status = manga_info.status
        return mi
