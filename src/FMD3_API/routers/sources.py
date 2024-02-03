from fastapi import APIRouter
from FMD3.api.sources import get_sources as sup_get_sources, get_source as sup_get_source
from FMD3.api.chapters import get_source_chapters as sup_get_source_chapters
router = APIRouter()


@router.get("/sources/")
async def get_sources():
    return sup_get_sources()


@router.get("/sources/{source_id}")
async def get_source(source_id: str):
    return sup_get_source(source_id=source_id)


@router.get("/sources/{source_id}/{series_id}")
async def get_chapters(source_id: str, series_id: str, get_from:int=None):
    """

    Args:
        source_id: The source id
        series_id: The series id
        get_from: If provided, it will return chapters that are greater than this number

    Returns:

    """
    return sup_get_source_chapters(source_id, series_id,get_from)

