from fastapi import APIRouter
from FMD3.api.chapters import get_chapters as sup_get_chapters, download_chapters as sup_download_chapters
router = APIRouter()


@router.get("/chapters/{series_id}")
async def get_chapters(series_id: str):
    return sup_get_chapters(series_id)


@router.get("/chapters/download/{source_id}/{series_id}")
async def download_chapters(source_id: str, series_id: str, chapter_ids: list[str] = None,output_path: str = None):
    return sup_download_chapters(source_id, series_id, chapter_ids, output_path)