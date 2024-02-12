import abc
import importlib
import io
import logging
import os
import pkgutil
import shutil
import sys
import zipfile

from importlib.metadata import entry_points

import requests

from .ISource import ISource
from ..constants import SOURCE_PATHS, EXTENSION_PATHS

"""Module with methods related with extensions"""

sources_factory: list[ISource] = []

logger = logging.getLogger(__name__)
def import_and_register_source(module_info: pkgutil.ModuleInfo):
    # sys.path.append(os.path.abspath(package_path))
    sys.path.append(str(EXTENSION_PATHS.resolve()))

    module_name = "MangaDex"  # Assuming this is the module name you want to import
    module_path = f"sources.{module_name}"

    try:
        importlib.invalidate_caches()
        module = importlib.import_module(module_path,package="sources")

        # Now you can access the Source variable from the imported module
        Source = module.Source
        sources_factory.append(module.Source())
        logger.info(f"Source module '{module_info.name}' imported and registered successfully.")
    except ImportError as e:
        logger.exception(f"Error importing source module '{module_info.name}': {e}")
    except Exception as e:
        logger.exception(f"Undhandled exception importing source module '{module_info.name}': {e}")
    finally:
        try:
            sys.path.remove(str(SOURCE_PATHS))
        except ValueError:
            pass

def reload_sources():
    sources_factory.clear()
    load_sources()

def load_sources():
    for module in list(pkgutil.iter_modules(path=[SOURCE_PATHS])):

        import_and_register_source(module)

def get_extension(name) -> ISource:
    for ext in sources_factory:
        if ext.NAME == name:
            return ext


def get_source(name=None, source_id=None) -> ISource|None:
    if name is None and source_id is None:
        raise ValueError("At least one parameter needs to be fulfilled: name or id. None provided")

    if source_id is not None:
        # Using next with a generator expression to find the extension by ID
        try:
            return next(ext for ext in sources_factory if ext.ID == source_id)
        except StopIteration:
            pass

    if name is not None:
        # Using next with a generator expression to find the extension by class name
        try:
            return next(ext for ext in sources_factory if ext.__class__.__name__ == name)
        except StopIteration:
            pass

    logging.getLogger(__name__).error(f"No extension found with name='{name}' and id='{source_id}'")
    # If no extension is found, you might want to return a default value or raise an exception
    return None


def get_source_by_id(source_id) -> ISource:
    for ext in sources_factory:
        if ext.ID == source_id:
            return ext


def get_sources_list() -> list[ISource]:
    return sources_factory


def list_sources() -> list[str]:
    return [ext.__class__.__name__ for ext in sources_factory]


def add_extension(extension: ISource):
    ...


def add_source(extension: ISource):
    # extension.init_settings()
    sources_factory.append(extension)


@abc.abstractmethod
def load_source():
    """
    This function acts as hook for extensions to run add_source passing it's own source class as parameter
    :param source:
    :return:
    """

def update_source(source_id):


    if not os.path.exists(SOURCE_PATHS):
        os.makedirs(SOURCE_PATHS)

    # "https://raw.githubusercontent.com/MangaManagerORG/FMD3-Extensions/repo/output"
    r = requests.get("https://raw.githubusercontent.com/MangaManagerORG/FMD3-Extensions/repo/output/" + source_id + ".zip")

    # Save the zip file

        # Extract the contents of the zip file directly from memory
    with zipfile.ZipFile(io.BytesIO(r.content), 'r') as zip_ref:
        top_level_folder = list({item.split('/')[0] + '/' for item in zip_ref.namelist() if '/' in item})[0]
        if os.path.exists(source_path:=os.path.join(SOURCE_PATHS,top_level_folder)):
            shutil.rmtree(source_path)
        zip_ref.extractall(SOURCE_PATHS)

    reload_sources()

def uninstall_source(source_id):
    for ext in sources_factory:
        if ext.ID == source_id:
            sources_factory.remove(ext)
            if os.path.exists(source_path := os.path.join(SOURCE_PATHS, ext.__class__.__name__)):
                shutil.rmtree(source_path)
    reload_sources()