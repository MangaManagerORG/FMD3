from typing import List

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import Response
from FMD3.api.api import Api
from FMD3.api.models.chapters import ChapterResponse, DownloadChapterForm

# from FMD3.api.chapters import get_chapters as sup_get_chapters, download_chapters as sup_download_chapters
router = APIRouter(prefix="/chapters", tags=["chapters"])


@router.get("/{series_id}", response_model=List[ChapterResponse])
async def get_chapters(series_id: str):
    return JSONResponse(jsonable_encoder(Api.get_chapters(series_id)))


@router.post("/download")
async def download_chapters(item:DownloadChapterForm):
    Api.download_chapters(item)
    return Response(content="Ok",status_code=200)
