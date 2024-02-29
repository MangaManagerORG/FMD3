import datetime
import enum
from FMD3.models.ddl_chapter_status import DLDChaptersStatus
from pydantic import BaseModel


class HangingTaskResponse(BaseModel):
    number:float
    volume:float|None
    title:str
    status:DLDChaptersStatus
    path:str
    added_at:datetime.datetime|None
    downloaded_at:datetime.datetime|None

    title:str=None
    source_id:str = None
    series_id:str = None
    chapter_id:str = None

