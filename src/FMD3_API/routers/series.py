from fastapi import APIRouter
from FMD3.api import get_series as sup_get_series, get_series_info as sup_get_series_info
router = APIRouter()


@router.get("/series/")
async def get_series():
    return sup_get_series()
    # return {"series": "series"}


@router.get("/series/info/{source_id}/{series_id}")
async def get_series_info(source_id: int, series_id: int):
    return sup_get_series_info(source_id, series_id)

