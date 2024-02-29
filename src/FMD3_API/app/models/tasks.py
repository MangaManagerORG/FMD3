import datetime
import enum

from pydantic import BaseModel


class HangingTaskResponse(BaseModel):
    number:int
    volume:int
    title:str
    status:enum.Enum
    path:str
    added_at:datetime.datetime
    downloaded_at:datetime.datetime

    title:str=None
    source_id:str = None
    series_id:str = None

