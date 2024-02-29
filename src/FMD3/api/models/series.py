import datetime
import enum
from typing import List, Optional
from FMD3.models.ddl_chapter_status import DLDChaptersStatus
from pydantic import BaseModel


class SeriesResponse(BaseModel):
    series_id: str
    enabled:bool
    source_id:str
    title:str
    status:DLDChaptersStatus|None
    max_chapter:int
    save_to:str
    dateadded:datetime.datetime|None
    datelastchecked:datetime.datetime|None
    datelastupdated:datetime.datetime|None


class SeriesInfoResponse(BaseModel):
    id: str
    source_id: str
    title: str
    alt_titles: List[str]
    description: str
    authors: List[str]
    artists: List[str]
    cover_url: str
    genres: List[str]
    demographic: str|None
    rating: float|None
    status: str
    chapters: list|None
    save_to: Optional[str]