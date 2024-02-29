from typing import Dict, List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
from FMD3.api.api import Api
from FMD3_API.app.models.tasks import HangingTaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/hanging", response_model=List[HangingTaskResponse])
async def get_hanging_tasks():
    return JSONResponse(jsonable_encoder(Api.get_hanging_tasks()))

@router.get("/recent", response_model=List[HangingTaskResponse])
async def get_recent_tasks():
    return JSONResponse(jsonable_encoder(Api.get_recent_tasks()))
