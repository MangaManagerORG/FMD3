from typing import Literal

import requests
from FMD3.api.series import get_series as sup_get_series, get_series_info as sup_get_series_info, \
    query_series as sup_query_series, get_series_folder_name as sup_get_series_folder_name, \
    get_cover as sup_get_series_cover
from FMD3.api.sources import get_sources as sup_get_sources, get_source as sup_get_source, get_available_sources as sup_get_available_sources, update_source as sup_update_source, uninstall_source as sup_uninstall_source
from FMD3.api.chapters import get_source_chapters as sup_get_source_chapters
from FMD3.api.chapters import get_chapters as sup_get_chapters, download_chapters as sup_download_chapters
from FMD3.api.settings import get_settings as sup_get_settings, update_settings as sup_update_settings, \
    update_save_to as sup_update_save_to
from FMD3.__version__ import __version__
from . import Api


class LocalApi(Api):
    @staticmethod
    def api_version():
        return f"Local:{__version__}"

    @staticmethod
    def get_series(sort=None, order: Literal["asc", "desc"] = "desc", limit=None):
        return sup_get_series()

    @staticmethod
    def get_series_info(source_id: str, series_id: str):
        return sup_get_series_info(source_id, series_id)

    @staticmethod
    def get_series_folder_name(website=None, manga=None, author=None, artist=None):
        return sup_get_series_folder_name(website, manga, author, artist)

    @staticmethod
    def query_series(source_id: str, query: str):
        return sup_query_series(source_id, query)

    @staticmethod
    def get_cover(source_id: str, request_url: str):
        return sup_get_series_cover(source_id, request_url)

    @staticmethod
    def get_sources():
        return sup_get_sources()

    @staticmethod
    def get_source(source_id: str):
        return sup_get_source(source_id=source_id)

    @staticmethod
    def get_source_chapters(source_id: str, series_id: str, get_from: int = None):
        return sup_get_source_chapters(source_id, series_id,get_from)

    @staticmethod
    def get_chapters(series_id: str):
        return sup_get_chapters(series_id)

    @staticmethod
    def download_chapters(source_id: str, series_id: str, chapter_ids: list[str] = None, output_path: str = None):
        return sup_download_chapters(source_id, series_id, chapter_ids, output_path)

    @staticmethod
    def get_settings():
        return sup_get_settings()

    @staticmethod
    def update_settings(settings):
        return sup_update_settings(settings)

    @staticmethod
    def update_settings_save_to(series_id: str, save_to: str):
        return sup_update_save_to(series_id, save_to)

    @staticmethod
    def get_available_sources():
        return sup_get_available_sources()

    @staticmethod
    def update_source(source_id):
        return sup_update_source(source_id)

    @staticmethod
    def uninstall_source(source_id):
        return sup_uninstall_source(source_id)