from typing import List

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from FMD3.api import SourcesResponse
from FMD3.api.api import Api
from FMD3.api.models.chapters import ChapterResponse, SourceChapterResponse

# from FMD3.api.sources import get_sources as sup_get_sources, get_source as sup_get_source, \
#     get_available_sources as sup_get_available_sources
# from FMD3.api.chapters import get_source_chapters as sup_get_source_chapters
# from FMD3.api.sources import check_source_updates as sup_check_source_updates

router = APIRouter(prefix="/sources", tags=["sources"])


@router.get("/", response_model=List[SourcesResponse])
async def get_sources():
    return JSONResponse(jsonable_encoder(Api.get_sources()))


@router.get("/{source_id}/{series_id}",tags=["chapters"],response_model=List[SourceChapterResponse])
async def get_chapters_from_source(source_id: str, series_id: str, get_from: int = -10):
    """

    Args:
        source_id: The source id
        series_id: The series id
        get_from: If provided, it will return chapters that are greater than this number

    Returns:

    """
    return JSONResponse(jsonable_encoder(Api.get_source_chapters(source_id, series_id, get_from)))

# @router.get("/sources/available/")
# async def get_available_sources():
#     return sup_get_available_sources()
#
#
# @router.get("/sources/check_updates/")
# async def check_source_updates():
#     return sup_check_source_updates()
