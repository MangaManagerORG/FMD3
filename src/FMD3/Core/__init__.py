from importlib.metadata import entry_points

from FMD3.Core.downloader import download
from FMD3.Extensions import get_extension


def load_extensions():
    display_eps = entry_points(group='FMD3_Extensions')
    for entry in display_eps:
        if entry.attr == "load_extension":
            module = entry.load()
            print(module)
            module()


