import pathlib


def get_sanitized_download(parent,website=None, manga=None, author=None, artist=None):
    return pathlib.Path(parent,
                        get_series_folder_name(website=website, manga=manga, author=author, artist=artist))