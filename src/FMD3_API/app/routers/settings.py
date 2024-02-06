from fastapi import APIRouter
from FMD3.api.settings import get_settings as sup_get_settings, update_settings as sup_update_settings, \
    update_save_to as sup_update_save_to

router = APIRouter()


@router.get("/settings/")
async def get_settings():
    return sup_get_settings()


@router.post("/settings/update/")
async def update_settings(settings: dict):
    return sup_update_settings(settings)


@router.post("/settings/update/save_to")
async def update_settings_save_to(series_id: str, save_to: str):
    return sup_update_save_to(series_id, save_to)
