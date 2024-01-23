import abc
from typing import final
from importlib.metadata import entry_points

from .ISource import ISource

"""Module with methods related with extensions"""

extesion_factory: list[ISource] = []



def load_sources():
    display_eps = entry_points(group='FMD3_Sources')
    for entry in display_eps:
        if entry.attr == "load_source":
            module = entry.load()
            module()


@abc.abstractmethod
def load_extension(extension: ISource):
    ...




def get_extension(name) -> ISource:
    for ext in extesion_factory:
        if ext.__class__.__name__ == name:
            return ext
def get_source(name) -> ISource:
    for ext in extesion_factory:
        if ext.__class__.__name__ == name:
            return ext

def get_sources_list() -> list[ISource]:
    return extesion_factory


def list_sources() -> list[str]:
    return [ext.__class__.__name__ for ext in extesion_factory]


def add_extension(extension: ISource):
    ...
    # extension.init_settings()
    # extesion_factory.append(extension)
def add_source(extension: ISource):
    # extension.init_settings()
    extesion_factory.append(extension)

@abc.abstractmethod
def load_source():
    """
    This function acts as hook for extensions to run add_source passing it's own source class as parameter
    :param source:
    :return:
    """

