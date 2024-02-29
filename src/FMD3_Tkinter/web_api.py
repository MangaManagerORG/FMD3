from typing import Literal

import requests

from FMD3.core.database import Series
from FMD3.api import ApiInterface
from FMD3.extensions.sources import ISource
from FMD3.extensions.sources.SearchResult import SearchResult
from FMD3_Tkinter.client_settings import Settings

session = requests.Session()


def host_url():
    return Settings().get("host")


class Api(ApiInterface):
    """

    """

    @staticmethod
    def api_version():
        pass

    """
    #########
    SERIES
    #########
    """

    @staticmethod
    def get_fav_series(sort=None, order: Literal["asc", "desc"] = "desc", limit=None) -> list[Series]:
        response = session.get(host_url() + "/series?sort=" + sort + "&order=" + order + "" + "&limit=" + limit)
        if response.status_code == 200:
            return response.json()
        else:
            # Handle errors if necessary
            return None

    @staticmethod
    def add_fav_series(source_id: str, series_id: str, output_path=None):
        ...

    @staticmethod
    def get_series_info(source_id: str, series_id: str):
        response = session.get(host_url() + f"/series/info?source_id={source_id}&series_id={series_id}")
        if response.status_code == 200:
            return response.json()
        else:
            # Handle errors if necessary
            return None

    @staticmethod
    def get_series_from_url(url: str):
        response = session.get(host_url() + "/series/")

        if response.status_code == 200:
            return response.json()
        else:
            # Handle errors if necessary
            return None

    @staticmethod
    def query_series(source_id: str, query: str):
        response = session.get(host_url() + f"/series/query?source_id={source_id}&query={query}")

        if response.status_code == 200:
            response.json()
            return [SearchResult(**item)
                    for item in response.json()]
        else:
            # Handle errors if necessary
            return []

    @staticmethod
    def get_series_folder_name(website=None, manga=None, author=None, artist=None) -> str:
        response = session.get(
            host_url() + f"/series/folder_name?manga={manga}&author={author}&website={website}&artist{artist}")
        if response.status_code == 200:
            return response.json()
        else:
            return None

    """
    #########
    CHAPTERS
    #########
    """

    @staticmethod
    def get_chapters(series_id: str):
        ...

    @staticmethod
    def download_chapters(source_id: str, series_id: str, chapter_ids: list[str] | Literal["all"] = None,
                          output_path: str = None, enable_series: bool = False, fav_series: bool = False):
        pass

    @staticmethod
    def get_source_chapters(source_id: str, series_id: str, get_from: int = None):
        pass

    """
    #########
    SOURCES
    #########
    """

    @staticmethod
    def get_sources() -> list[ISource]:
        pass

    @staticmethod
    def get_source(source_id: str):
        pass

    @staticmethod
    def get_available_sources():
        pass

    @staticmethod
    def update_source(source_id):
        pass

    @staticmethod
    def uninstall_source(source_id):
        pass

    @staticmethod
    def check_source_updates():
        pass

    """
    #########
    SETTINGS
    #########
    """

    @staticmethod
    def get_settings():
        pass

    @staticmethod
    def update_settings(settings):
        pass

    @staticmethod
    def update_settings_save_to(series_id: str, save_to: str):
        pass

    """
    #########
    TASKS
    #########
    """

    @staticmethod
    def get_hanging_tasks():
        pass

    @staticmethod
    def get_active_tasks():
        pass

    @staticmethod
    def get_recent_tasks():
        pass
