from sqlalchemy import Column, Integer, Boolean, String, DateTime, Text, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship

from .Session import Session
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

    @property
    def max_chapter_number(self):
        # Retrieve the max number from the DLDChapters table

        session = Session()
        max_number = session.query(DLDChapters.number).filter(
            DLDChapters.series_id == self.series_id).order_by(
            DLDChapters.number.desc()).first()

        # Return the max number if it exists, otherwise return None
        if max_number:
            return max_number.number
        else:
            return None

class DLDChapters(Base):
    """Represents a downloaded chapter"""
    __tablename__ = 'DLDChapters'
    # _id = Column(Integer, autoincrement=True)
    chapter_id = Column(String(30), primary_key=True)
    series_id = Column(String(30), ForeignKey("series.series_id"), primary_key=True)

    number = Column(SmallInteger)
    volume = Column(SmallInteger)
    title = Column(Text)

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
