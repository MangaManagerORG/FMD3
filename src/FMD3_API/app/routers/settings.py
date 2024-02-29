from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from FMD3.api.api import Api

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("/")
async def get_settings():
    res = JSONResponse(Api.get_settings())
    return res


@router.post("/settings/update/")
async def update_settings(data: str = Body(...)):
    Api.update_settings(data)
    return {"message": "Received JSON data successfully"}
#
#
# @router.post("/settings/update/save_to")
# async def update_settings_save_to(series_id: str, save_to: str):
#     return sup_update_save_to(series_id, save_to)
