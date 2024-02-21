from pathlib import Path

from FMD3_Tkinter import api


def get_sanitized_download(parent, website=None, manga=None, author=None, artist=None):
    return Path(parent,
                api.get_series_folder_name(website=website, manga=manga, author=author, artist=artist))