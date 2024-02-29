import datetime
from typing import Literal

from pydantic import BaseModel

from FMD3.models.ddl_chapter_status import DLDChaptersStatus


class ChapterResponse(BaseModel):
    chapter_id:str
    series_id:str
    volume:float|None
    number:int
    title:str|None
    status:DLDChaptersStatus
    path:str
    added_at: datetime.datetime | None
    downloaded_at:datetime.datetime | None
class SourceChapterResponse(BaseModel):
    chapter_id:str
    volume:float|None
    number:float
    title:str|None
    pages:int
    scanlator:str|None
# {
#             "chapter_id": chapter.chapter_id,
#             "series_id": chapter.series_id,
#             "volume": chapter.volume,
#             "number": chapter.number,
#             "title": chapter.title,
#             "status": DLDChaptersStatus(chapter.status),
#             "path": chapter.path,
#             "download_date": chapter.added_at
#         }

class DownloadChapterForm(BaseModel):
    output_path:str
    series_id:str
    source_id:str
    fav_series:bool
    enable_series:bool
    chapter_ids:list[str] | Literal["all"]