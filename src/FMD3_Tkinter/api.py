from typing import Literal

import requests

from FMD3_Tkinter.settings import Settings

session = requests.Session()
host_url = Settings().get("host")


def get_series(sort=None, order: Literal["asc", "desc"] = "desc", limit=None):
    return session.get(host_url + "/series/").json()


def get_series_info(source_id: str, series_id: str):
    return session.get(host_url + f"/series/info/{source_id}/{series_id}").json()


def get_series_folder_name(website=None, manga=None, author=None, artist=None):
    return session.get(
        host_url + f"/series/folder_name?website={website}&manga={manga}&author={author}&artist={artist}").json()


def query_series(source_id: str, query: str):
    return session.get(host_url + f"/series/query/{source_id}/{query}").json()


def get_cover(source_id: str, request_url: str):
    return session.get(host_url + f"/series/cover/{source_id}?request_url={request_url}").json()


def get_sources():
    return session.get(host_url + "/sources/").json()


def get_source(source_id: str):
    return session.get(host_url + f"/sources/{source_id}").json()


def get_source_chapters(source_id: str, series_id: str, get_from: int = None):
    return session.get(host_url + f"/sources/{source_id}/{series_id}?get_from={get_from}").json()


def get_chapters(series_id: str):
    return session.get(host_url + f"/chapters/{series_id}").json()


def download_chapters(source_id: str, series_id: str, chapter_ids: list[str] = None, output_path: str = None):
    return session.get(
        host_url + f"/chapters/download/{source_id}/{series_id}?chapter_ids={chapter_ids}&output_path={output_path}").json()


def get_settings():
    r = session.get(host_url + "/settings/")
    return r.json()


def update_settings(settings):
    return session.post(host_url + "/settings/", json=settings).json()


def update_settings_save_to(series_id: str, save_to: str):
    return session.post(host_url + f"/settings/update/save_to?series_id={series_id}&save_to={save_to}").json()
