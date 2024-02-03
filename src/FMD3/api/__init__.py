import json
import pathlib

from FMD3.core import database as db
from FMD3.core.settings import Settings, Keys
from FMD3.core.utils import get_series_folder_name
from FMD3.sources import get_source as sup_get_source


def get_sanitized_download(website=None, manga=None, author=None, artist=None):
    return pathlib.Path(Settings().get(Keys.DEFAULT_DOWNLOAD_PATH),
                        get_series_folder_name(website=website, manga=manga, author=author, artist=artist))


def get_cover(source_id, request_url):
    source = sup_get_source(source_id=source_id)
    return source.session.get(request_url)


def get_settings():
    return Settings().to_json()


def update_settings(new_settings):
    new_set = json.loads(new_settings)
    Settings().update(new_set)


def update_save_to(series_id, new_value):
    if new_value is None:
        return
    db.Session().query(db.Series).filter_by(series_id=series_id).one_or_none().save_to = new_value
    db.Session().commit()
