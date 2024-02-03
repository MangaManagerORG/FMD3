import json

from FMD3 import Settings
from FMD3.core import database as db


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