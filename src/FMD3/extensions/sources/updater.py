import logging

import requests

from . import sources_factory, get_source
from packaging import version
installed_sources = {}

logger = logging.getLogger(__name__)

def check_source_updates():
    for source in sources_factory:
        installed_sources[source.ID] = {
            "name": source.NAME,
            "id": source.ID,
            "category": source.CATEGORY,
            "version": version.parse(source.VERSION),
        }

    r = requests.get("https://raw.githubusercontent.com/MangaManagerORG/FMD3-Extensions/repo/extensions.json")
    available_sources = r.json()

    for source in installed_sources:
        if source in available_sources:
            if version.parse(available_sources[source]["version"]) > installed_sources[source]["version"]:
                logger.warning(f"New version of {installed_sources[source]['name']} available: {available_sources[source]['version']}")
                get_source(source_id=source)._has_updates = available_sources[source]['version']