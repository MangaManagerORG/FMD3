import enum

from sqlalchemy import Column, String, ForeignKey, SmallInteger, Text, Integer, DateTime, func

from ...database import Base
from FMD3.models.chapter import Chapter
from FMD3.models.ddl_chapter_status import DLDChaptersStatus as _DLDChaptersStatus

class DLDChaptersStatus(enum.Enum):
    NOT_DOWNLOADED = 0
    DOWNLOADED = 1  # Chapter completed
    ADDED_TO_QUEUE = 2  # added to queue. (If program exists these will be loaded first on next scan)
    SKIPPED = 3  # (file existing and apparently correct)
    ERRORED = 4  # Chapter downloads that errored. #Todo: reload them in tasks (maybe on next scan? add retry counter?)

    def as_name(self):
        return self.name.replace("_", " ")


class DLDChapters(Base):
    """Represents a downloaded chapter"""
    __tablename__ = 'DLDChapters'
    # _id = Column(Integer, autoincrement=True)
    chapter_id = Column(String(30), primary_key=True, nullable=False)
    series_id = Column(String(30), ForeignKey("series.series_id"), primary_key=True, nullable=False)

    number = Column(SmallInteger)
    volume = Column(SmallInteger)
    title = Column(Text)
    status = Column(Integer, default=_DLDChaptersStatus.NOT_DOWNLOADED.value)
    path = Column(Text)
    downloaded_at = Column(DateTime, server_default=func.now())

    # series = relationship("Series",back_populates="DLDChapters")

    @staticmethod
    def from_chapter(chapter: Chapter, series_id: str):
        ret = DLDChapters()
        ret.chapter_id = chapter.chapter_id
        ret.series_id = series_id
        ret.number = chapter.number
        ret.title = chapter.title
        ret.volume = chapter.volume
        return ret
    # series_id = Column(Integer, ForeignKey('series.chapter_id'))
    # series = orm.relationship('Series', backref='dld_chapters')
