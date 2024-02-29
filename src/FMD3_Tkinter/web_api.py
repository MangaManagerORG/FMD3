from typing import Literal, List

import requests

from FMD3.api.models.chapters import ChapterResponse, SourceChapterResponse, DownloadChapterForm
from FMD3.api.models.series import SeriesResponse
from FMD3.api import ApiInterface, SourcesResponse
from FMD3.extensions.sources import ISource
from FMD3.extensions.sources.SearchResult import SearchResult
from FMD3.models.ddl_chapter_status import DLDChaptersStatus
from FMD3.api.models.tasks import HangingTaskResponse
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
    def get_fav_series(sort=None, order: Literal["asc", "desc"] = "desc", limit=None) -> list[SeriesResponse]:
        response = session.get(
            host_url() + f"/series?sort={sort}&order={order}{f'&limit={limit}' if limit is not None else ''}")

        if response.status_code == 200:
            return [SeriesResponse(**item)
                    for item in response.json()]
        else:
            # Handle errors if necessary
            return []

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
        response = session.get(
            host_url() + f"/chapters/{series_id}")
        if response.status_code == 200:
            return [ChapterResponse(**item)
                    for item in response.json()]
        else:
            return None

    @staticmethod
    def download_chapters(item:DownloadChapterForm):
        response = session.post(host_url() + f"/chapters/download",json=item.dict())
        if response.status_code == 200:
            return True

    @staticmethod
    def get_source_chapters(source_id: str, series_id: str, get_from: int = -1) -> List[SourceChapterResponse]:
        response = session.get(
            host_url() + f"/sources/{source_id}/{series_id}?get_from={get_from}")
        if response.status_code == 200:
            return [SourceChapterResponse(**item)
                    for item in response.json()]
        else:
            return None

    """
    #########
    SOURCES
    #########
    """

    @staticmethod
    def get_sources() -> List[SourcesResponse]:
        response = session.get(
            host_url() + f"/sources")
        if response.status_code == 200:
            return [SourcesResponse(**item)
                    for item in response.json()]
        else:
            return None

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
        response = session.get(host_url() + "/settings")
        if response.status_code == 200:
            return response.json()
        else:
            # Handle errors if necessary
            return None

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
        response = session.get(host_url() + "/tasks/hanging")
        hanging_tasks = [
            HangingTaskResponse(
                number=item['number'],
                volume=item['volume'],
                title=item['title'],
                status=DLDChaptersStatus(item['status']),  # Replace YourEnum with the actual Enum class
                path=item['path'],
                added_at=item['added_at'],
                downloaded_at=item['downloaded_at']
            )
            for item in response.json()
        ]
        if response.status_code == 200:
            return hanging_tasks
        else:
            # Handle errors if necessary
            return None

    @staticmethod
    def get_active_tasks():
        pass

    @staticmethod
    def get_recent_tasks():
        response = session.get(host_url() + "/tasks/recent")
        hanging_tasks = [
            HangingTaskResponse(
                number=item['number'],
                volume=item['volume'],
                title=item['title'],
                status=DLDChaptersStatus(item['status']),  # Replace YourEnum with the actual Enum class
                path=item['path'],
                added_at=item['added_at'],
                downloaded_at=item['downloaded_at']
            )
            for item in response.json()
        ]
        if response.status_code == 200:
            return hanging_tasks
        else:
            # Handle errors if necessary
            return None
