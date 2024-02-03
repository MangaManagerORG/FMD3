from FMD3 import get_source as sup_get_source
from FMD3.sources import get_sources_list


def get_sources():
    return [
        {
            "id": source.ID,
            "name": source.NAME
        }
        for source in get_sources_list()
    ]


def get_source(name=None, source_id=None):
    src = sup_get_source(name=name, source_id=source_id)
    source = {
        "id": src.ID,
        "name": src.NAME,
        "root_url": src.ROOT_URL,
        "category": src.CATEGORY,
        "maxtasklimit": src.MaxTaskLimit
    }
    return source



