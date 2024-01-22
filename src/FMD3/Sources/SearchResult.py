import dataclasses


@dataclasses.dataclass
class SearchResult():
    series_id:str
    title:str
    loc_title:str
    year:int
    cover_url:str
