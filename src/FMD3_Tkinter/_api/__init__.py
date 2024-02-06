from abc import abstractmethod
from typing import Literal


class Api:
    @staticmethod
    @abstractmethod
    def get_series(sort=None, order: Literal["asc", "desc"] = "desc", limit=None):
        ...

    @staticmethod
    @abstractmethod
    def get_series_info(source_id: str, series_id: str):
        ...

    @staticmethod
    @abstractmethod
    def get_series_folder_name(website=None, manga=None, author=None, artist=None):
        ...

    @staticmethod
    @abstractmethod
    def query_series(source_id: str, query: str):
        ...

    @staticmethod
    @abstractmethod
    def get_cover(source_id: str, request_url: str):
        ...

    @staticmethod
    @abstractmethod
    def get_sources():
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
    def download_chapters(source_id: str, series_id: str, chapter_ids: list[str] = None, output_path: str = None):
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
    def update_settings_save_to(series_id:str, save_to:str):
        ...
