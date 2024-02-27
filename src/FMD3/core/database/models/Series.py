import enum

from sqlalchemy import Column, Text, Integer, Boolean, String, DateTime, func, Enum
from sqlalchemy.orm import relationship

from FMD3.core.database import Base


class SeriesStatus(enum.Enum):
    ONGOING = 0
    FINISHED = 1
    FINISHED_AND_DOWNLOADED = 2


class Series(Base):
    __tablename__ = 'series'

    # id = Column(Integer, autoincrement=True)
    series_id = Column(Text, nullable=False, primary_key=True)  # Used
    enabled = Column(Boolean)  # Used
    favourited = Column(Boolean, default=False)
    source_id = Column(String(255),  nullable=False)  # Used
    title = Column(Text, nullable=False)  # Used
    status = Column(Enum(SeriesStatus))  # Used

    save_to = Column(Text)  # will be used

    dateadded = Column(DateTime, server_default=func.now())
    datelastchecked = Column(DateTime)
    datelastupdated = Column(DateTime)

    chapters = relationship("DLDChapters", backref="series")
    url = Column(Text)
