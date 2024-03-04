from typing import List

import requests

from FMD3 import get_source as sup_get_source
from FMD3.api import SourcesResponse
from FMD3.extensions.sources import get_sources_list, update_source as sup_update_source, reload_sources
from FMD3.extensions.sources import check_source_updates, uninstall_source as sup_uninstall_source

# Using the imports so IDE won't clear them accidentally.
__used_imports = f"{check_source_updates}"


def get_sources() -> List[SourcesResponse]:
    return [
        SourcesResponse(**{"ID": source.ID,
                           "CATEGORY": source.CATEGORY,
                           "NAME": source.NAME,
                           "VERSION": source.VERSION,
                           "ROOT_URL": source.ROOT_URL,
                           "HAS_UPDATES": source._has_updates})
        for source in get_sources_list()
    ]


def get_source(name=None, source_id=None) -> SourcesResponse:
    source = sup_get_source(name=name, source_id=source_id)
    if source is None:
        return None
    # source = {
    #     "id": src.ID,
    #     "name": src.NAME,
    #     "root_url": src.ROOT_URL,
    #     "category": src.CATEGORY,
    #     "maxtasklimit": src.MaxTaskLimit,
    #     "version": src.VERSION,
    #     "has_updates": src._has_updates,
    # }
    return SourcesResponse(**{"ID": source.ID,
                              "CATEGORY": source.CATEGORY,
                              "NAME": source.NAME,
                              "VERSION": source.VERSION,
                              "ROOT_URL": source.ROOT_URL,
                              "HAS_UPDATES": source._has_updates})


def get_source_from_url(url: str) -> str:
    for source in get_sources_list():
        if source.is_url_from_source(url):
            return source.ID


def get_available_sources():
    return requests.get("https://raw.githubusercontent.com/MangaManagerORG/FMD3-Extensions/repo/extensions.json").json()


def update_source(sources_ids: list[str]):
    for source_id in sources_ids:
        sup_update_source(source_id=source_id, do_reload_sources=False)
    reload_sources()
    return True


def uninstall_sources(sources_ids: list[str]):
    for source_id in sources_ids:
        sup_uninstall_source(source_id=source_id, do_reload_sources=False)
