import enum

from sqlalchemy import Column, Integer, Boolean, String, DateTime, Text, ForeignKey, SmallInteger, func
from sqlalchemy.orm import relationship

from .base import Base
from ...Models.Chapter import Chapter


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
    dateadded = Column(DateTime)
    datelastchecked = Column(DateTime)
    datelastupdated = Column(DateTime)

    chapters = relationship("DLDChapters", backref="series")


class DLDChaptersStatus(enum.Enum):
    NOT_DOWNLOADED = 0
    DOWNLOADED = 1 # Chapter completed
    ADDED_TO_QUEUE = 2 # added to queue. (If program exists these will be loaded first on next scan)
    SKIPPED = 3 # (file existing and apparently correct)
    ERRORED = 4 # Chapter downloads that errored. #Todo: reload them in tasks (maybe on next scan? add retry counter?)



class DLDChapters(Base):
    """Represents a downloaded chapter"""
    __tablename__ = 'DLDChapters'
    # _id = Column(Integer, autoincrement=True)
    chapter_id = Column(String(30), primary_key=True, nullable=False)
    series_id = Column(String(30), ForeignKey("series.series_id"), primary_key=True, nullable=False)

    number = Column(SmallInteger)
    volume = Column(SmallInteger)
    title = Column(Text)
    status = Column(
        Integer)
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
