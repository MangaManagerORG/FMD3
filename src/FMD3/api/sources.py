import io
import os
import shutil
import zipfile

import requests

from FMD3 import get_source as sup_get_source
from FMD3.sources import get_sources_list


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


def get_source(name=None, source_id=None):
    src = sup_get_source(name=name, source_id=source_id)
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


def update_source(source_id="d07c9c2425764da8ba056505f57cf40c"):
    output_path = r"C:\Users\galla\PycharmProjects\FMD2_Port\test_extensions"

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    "https://raw.githubusercontent.com/MangaManagerORG/FMD3-Extensions/repo/output"
    r = requests.get("https://raw.githubusercontent.com/MangaManagerORG/FMD3-Extensions/repo/output/" + source_id + ".zip")

    # Save the zip file

        # Extract the contents of the zip file directly from memory
    with zipfile.ZipFile(io.BytesIO(r.content), 'r') as zip_ref:
        top_level_folder = list({item.split('/')[0] + '/' for item in zip_ref.namelist() if '/' in item})[0]
        if os.path.exists(source_path:=os.path.join(output_path,top_level_folder)):
            shutil.rmtree(source_path)
        zip_ref.extractall(output_path)