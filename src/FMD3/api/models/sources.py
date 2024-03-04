from pydantic import BaseModel


class SourcesResponse(BaseModel):
    CATEGORY: str
    ID: str
    NAME: str
    VERSION: str | None
    ROOT_URL: str | None
    HAS_UPDATES: bool|str | None


class SearchResult(BaseModel):
    series_id:str
    title:str
    loc_title:str|None
    year:int|None
    cover_url:str
