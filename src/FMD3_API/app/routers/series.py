from fastapi import APIRouter
from fastapi.openapi.models import Response

from FMD3.api.series import get_fav_series as sup_get_series, get_series_info as sup_get_series_info, \
    query_series as sup_query_series, get_series_folder_name as sup_get_series_folder_name, \
    get_series_from_url as sup_get_series_from_url

router = APIRouter()


@router.get("/series/")
async def get_series():
    return sup_get_series()
    # return {"series": "series"}


@router.get("/series/info/{source_id}/{series_id}")
async def get_series_info(source_id: str, series_id: str):
    return sup_get_series_info(source_id, series_id)


@router.get("/series/query/{source_id}/{query}")
async def query_series(source_id: str, query: str):
    return sup_query_series(source_id, query)


@router.get("/series/folder_name")
async def get_series_folder_name(website=None, manga=None, author=None, artist=None):
    return sup_get_series_folder_name(website, manga, author, artist)

@router.get("/series/url")
async def get_series_from_url(url:str):
    return sup_get_series_from_url(url)

@router.get("/series/cover/{source_id}}",
            responses={
                200: {
                    "content": {
                        "image/jpeg": {}
                    }
                }
            },
            response_class=Response
            )
async def get_series_cover(source_id: str, request_url: str):
    image_bytes = sup_get_series_cover(source_id, request_url)
    return Response(content=image_bytes, media_type="image/jpeg")
