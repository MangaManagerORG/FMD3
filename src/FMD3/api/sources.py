import io
import os
import shutil
import zipfile

import requests

from FMD3 import get_source as sup_get_source
from FMD3.sources import get_sources_list, update_source as sup_update_source, uninstall_source as sup_uninstall_source
from FMD3.sources.updater import check_source_updates as sup_check_source_updates


def get_sources():
    return [
        {
            "id": source.ID,
            "name": source.NAME,
            "version": source.VERSION,
            "has_updates": source._has_updates,
        }
        for source in get_sources_list()
    ]


def get_source(name=None, source_id=None) -> dict or None:
    src = sup_get_source(name=name, source_id=source_id)
    if src is None:
        return None
    source = {
        "id": src.ID,
        "name": src.NAME,
        "root_url": src.ROOT_URL,
        "category": src.CATEGORY,
        "maxtasklimit": src.MaxTaskLimit,
        "version": src.VERSION,
        "has_updates": src._has_updates,
    }
    return source


def get_available_sources():
    return requests.get("https://raw.githubusercontent.com/MangaManagerORG/FMD3-Extensions/repo/sources.json").json()


def update_source(source_id):
    sup_update_source(source_id=source_id)

def uninstall_source(source_id):
    sup_uninstall_source(source_id=source_id)

def check_source_updates():
    sup_check_source_updates()