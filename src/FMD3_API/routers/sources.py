from fastapi import APIRouter
from FMD3.api.sources import get_sources as sup_get_sources, get_source as sup_get_source

router = APIRouter()


@router.get("/sources/")
async def get_sources():
    return sup_get_sources()


@router.get("/sources/{source_id}")
async def get_source(source_id: str):
    return sup_get_source(source_id=source_id)
