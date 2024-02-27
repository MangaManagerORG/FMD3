from abc import abstractmethod
from typing import Literal

from FMD3.extensions.sources import ISource
from FMD3.extensions.sources.SearchResult import SearchResult


class ApiInterface:
    @staticmethod
    @abstractmethod
    def api_version():
        ...

    @staticmethod
    @abstractmethod
    def get_fav_series(sort=None, order: Literal["asc", "desc"] = "desc", limit=None):
        ...

    @staticmethod
    @abstractmethod
    def add_fav_series(source_id: str, series_id: str, output_path=None):
        ...

    @staticmethod
    @abstractmethod
    def get_series_info(source_id: str, series_id: str):
        ...

    @staticmethod
    @abstractmethod
    def get_series_folder_name(website=None, manga=None, author=None, artist=None) -> str:
        ...

    @staticmethod
    @abstractmethod
    def query_series(source_id: str, query: str) -> list[SearchResult]:
        ...

    @staticmethod
    @abstractmethod
    def get_sources() -> list[ISource]:
        ...

    @staticmethod
    @abstractmethod
    def get_source(source_id: str):
        ...

    @staticmethod
    @abstractmethod
    def get_source_chapters(source_id: str, series_id: str, get_from: int = None):
        ...

    @staticmethod
    @abstractmethod
    def get_chapters(series_id: str):
        ...

    @staticmethod
    @abstractmethod
    def download_chapters(source_id: str, series_id: str, chapter_ids: list[str]|Literal["all"] = None, output_path: str = None,
                          enable_series: bool=False, fav_series:bool=False):
        ...

    @staticmethod
    @abstractmethod
    def get_settings():
        ...

    @staticmethod
    @abstractmethod
    def update_settings(settings):
        ...

    @staticmethod
    @abstractmethod
    def update_settings_save_to(series_id: str, save_to: str):
        ...

    @staticmethod
    @abstractmethod
    def get_available_sources():
        ...

    @staticmethod
    @abstractmethod
    def update_source(source_id):
        ...

    @staticmethod
    @abstractmethod
    def uninstall_source(source_id):
        ...

    @staticmethod
    @abstractmethod
    def check_source_updates():
        ...

    @staticmethod
    @abstractmethod
    def get_series_from_url(url: str):
        ...