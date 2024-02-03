from fastapi import APIRouter
from FMD3.api.series import get_series as sup_get_series, get_series_info as sup_get_series_info, \
    query_series as sup_query_series

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