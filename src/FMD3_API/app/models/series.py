from pydantic import BaseModel
from typing import List, Optional

from FMD3.core.database import Series
from FMD3.extensions.sources.SearchResult import SearchResult


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


class SearchResultList(BaseModel):
    results: List[SearchResult]
