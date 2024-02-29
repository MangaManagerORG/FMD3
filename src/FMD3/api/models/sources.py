from pydantic import BaseModel


class SourcesResponse(BaseModel):
    CATEGORY: str
    ID: str
    NAME: str
    VERSION: str | None
    ROOT_URL: str | None
    HAS_UPDATES: bool|str | None

