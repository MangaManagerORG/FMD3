from typing import Literal

import requests


def get_series(sort=None, order: Literal["asc", "desc"] = "desc", limit=None):
    return requests.get("http://localhost:8000/series/")


def get_series_info(source_id: str, series_id: str):
    return requests.get(f"http://localhost:8000/series/info/{source_id}/{series_id}")


def query_series(source_id: str, query: str):
    return requests.get(f"http://localhost:8000/series/query/{source_id}/{query}")


def get_sources():
    return requests.get("http://localhost:8000/sources/")


def get_source(source_id: str):
    return requests.get(f"http://localhost:8000/sources/{source_id}")