"https://mangadex.org/title/41aea7f6-5ede-45d9-b7e6-7729acad4ea2/furyou-idol-chan"
from FMD3.Core.database import get_session
from FMD3.Core.database.models import Series
from FMD3.Models.MangaInfo import MangaInfo

def add_favorite_series(manga:MangaInfo):
    session = get_session()

    series = Series(series_id=)

