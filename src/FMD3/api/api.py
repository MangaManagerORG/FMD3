from . import ApiInterface
from .routes.chapters import *
from .routes.series import *
from .routes.sources import *
from .routes.settings import *
from .routes.tasks import *
from FMD3.__version__ import __version__


class Api(ApiInterface):
    """
    Class wrapping all api related methods
    """
    @staticmethod
    def api_version():
        return __version__

    """
    Chapter definitions
    """
    get_chapters = staticmethod(get_chapters)
    get_source_chapters = staticmethod(get_source_chapters)
    download_chapters = staticmethod(download_chapters)

    """
    Series definitions
    """

    get_fav_series = staticmethod(get_fav_series)
    add_fav_series = staticmethod(add_series_favourite)
    get_series_info = staticmethod(get_series_info)
    query_series = staticmethod(query_series)
    get_series_folder_name = staticmethod(get_series_folder_name)
    get_series_from_url = staticmethod(get_series_from_url)

    """
    Sources definitions
    """
    get_sources = staticmethod(get_sources)
    # get_source = staticmethod(get_source)
    get_source_from_url = staticmethod(get_source_from_url)
    @staticmethod
    def get_available_sources():
        return requests.get(
            "https://raw.githubusercontent.com/MangaManagerORG/FMD3-Extensions/repo/extensions.json").json()

    update_source = staticmethod(update_source)
    uninstall_source = staticmethod(uninstall_source)
    check_source_updates = staticmethod(check_source_updates)

    """
    Settings definitions
    """

    get_settings = staticmethod(get_settings)
    update_settings = staticmethod(update_settings)
    update_settings_save_to = staticmethod(update_save_to)


    """
    Tasks definition
    """

    get_active_tasks = staticmethod(get_active_tasks)
    get_recent_tasks = staticmethod(get_recent_tasks)
    get_hanging_tasks = staticmethod(get_hanging_tasks)
