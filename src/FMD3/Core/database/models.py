from sqlalchemy import Column, Integer, Boolean, String, DateTime, Text, ForeignKey, SmallInteger
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


class DLDChapters(Base):
    """Represents a downloaded chapter"""
    __tablename__ = 'DLDChapters'
    # _id = Column(Integer, autoincrement=True)
    chapter_id = Column(String(30), primary_key=True, nullable=False)
    series_id = Column(String(30), ForeignKey("series.series_id"), primary_key=True, nullable=False)

    number = Column(SmallInteger)
    volume = Column(SmallInteger)
    title = Column(Text)

    # series = relationship("Series",back_populates="DLDChapters")

    @staticmethod
    def from_chapter(chapter: Chapter, series_id: str):

        return
    # series_id = Column(Integer, ForeignKey('series.chapter_id'))
    # series = orm.relationship('Series', backref='dld_chapters')

# Series()
