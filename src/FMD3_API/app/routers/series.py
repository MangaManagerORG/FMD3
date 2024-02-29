from typing import Literal, List

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from FMD3.api import ApiInterface

from FMD3.extensions.sources.SearchResult import SearchResult
from FMD3.api.models.series import SeriesInfoResponse, SeriesResponse
from FMD3.api.api import Api

Api: ApiInterface
router = APIRouter(prefix="/series", tags=["series"])


@router.get("/", response_model=List[SeriesResponse])
async def get_fav_series(sort=None, order: Literal["asc", "desc"] = "desc", limit=None):
    return JSONResponse(jsonable_encoder(Api.get_fav_series(sort=sort, order= order, limit=limit)))


@router.get("/info", response_model=SeriesInfoResponse)
async def get_series_info(source_id: str, series_id: str):
    return Api.get_series_info(source_id, series_id)


@router.get("/url", response_model=SeriesInfoResponse)
async def get_series_from_url(url:str):
    """
    Gets series info from the url
    Args:
        url:

    Returns:

    """
    return JSONResponse(jsonable_encoder(Api.get_series_from_url(url)))


@router.get("/query", response_model=List[SearchResult])
async def query_series(source_id: str, query: str):
    res = Api.query_series(source_id, query)
    return JSONResponse(jsonable_encoder(res))


@router.get("/folder_name", response_model=str)
async def get_series_folder_name(website=None, manga=None, author=None, artist=None):
    """
    Helper endpoint to get the parsed foldername of the series
    Args:
        website:
        manga:
        author:
        artist:

    Returns:

    """
    return Api.get_series_folder_name(website=website, manga=manga, author=author, artist=artist)
