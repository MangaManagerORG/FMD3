# from FMD3.Core import logging
import importlib
import pkgutil

import FMD3.Extensions

from importlib.metadata import entry_points
def load_extensions():
    display_eps = entry_points(group='FMD3.Extensions')
    for entry in display_eps:

        if entry.attr == "load_extension":
            entry.load()()

def hello():
    # print("Hello World")
    # logging.getLogger().info("Test")
    load_extensions()
