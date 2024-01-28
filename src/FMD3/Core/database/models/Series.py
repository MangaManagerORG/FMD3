import enum

from sqlalchemy import Column, Text, Integer, Boolean, String, SmallInteger, DateTime, func
from sqlalchemy.orm import relationship

from FMD3.Core.database import Base


class SeriesStatus(enum.Enum):
    ONGOING = 0
    FULLY_DOWNLOADED = 1


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

    dateadded = Column(DateTime, server_default=func.now())
    datelastchecked = Column(DateTime)
    datelastupdated = Column(DateTime)

    chapters = relationship("DLDChapters", backref="series")
