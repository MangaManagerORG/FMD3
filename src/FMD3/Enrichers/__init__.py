"""
Module that holds the interfaces for the metadata enrichers
"""
from abc import abstractmethod
from importlib.metadata import entry_points

from ComicInfo import ComicInfo

from .IEnricher import IEnricher
from ..Models.Chapter import Chapter

enricher_factory: list[IEnricher] = []


# def load_enrichers():
#     display_eps = entry_points(group='FMD3_Enrichers')
#     for entry in display_eps:
#         if entry.attr == "load_enricher":
#             module = entry.load()
#             module()
# def load_enricher(module:IEnricher):
#     enricher_factory.append(module)


def get_enricher(name) -> IEnricher:
    for ext in enricher_factory:
        if ext.__class__.__name__ == name:
            return ext


def get_enricher_list() -> list[IEnricher]:
    return enricher_factory


def list_enrichers() -> list[str]:
    return [ext.__class__.__name__ for ext in enricher_factory]


def add_source(extension: IEnricher):
    # extension.init_settings()
    enricher_factory.append(extension)


@abstractmethod
def load_source():
    """
    This function acts as hook for extensions to run add_source passing it's own source class as parameter
    :param source:
    :return:
    """


def iterate_enrichers(manga_data, chapter: Chapter):
    final_comic_info = ComicInfo()
    for enricher in enricher_factory:
        manga_data, chapter, final_comic_info = enricher.process(manga_data, chapter, final_comic_info)
    return final_comic_info
