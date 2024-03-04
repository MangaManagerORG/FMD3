import abc
import importlib
import io
import logging
import os
import pkgutil
import shutil
import sys
import zipfile

import requests
from packaging import version

from .ISource import ISource
from FMD3.constants import SOURCE_PATHS, EXTENSION_PATHS

"""Module with methods related with extensions"""

sources_factory: list[ISource] = []
installed_sources = {}
logger = logging.getLogger(__name__)


def import_and_register_source(module_info: pkgutil.ModuleInfo):
    # sys.path.append(os.path.abspath(package_path))
    sys.path.append(str(EXTENSION_PATHS.resolve()))

    module_name = module_info.name  # Assuming this is the module name you want to import
    module_path = f"sources.{module_name}.{module_name}"

    try:
        importlib.invalidate_caches()
        module = importlib.import_module(module_path, package="sources")
        ext_class = module.__getattribute__(module_name)()
        ext_class.VERSION = module.__version__
        # module.load_source()
        add_source(ext_class)

        # Now you can access the Source variable from the imported module
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


def get_source(name=None, source_id=None) -> ISource | None:
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
    logger.info(f"Added extension '{extension.NAME}' version '{extension.VERSION}' - ID: {extension.ID}")


@abc.abstractmethod
def load_source():
    """
    This function acts as hook for extensions to run add_source passing it's own source class as parameter
    :param source:
    :return:
    """


def check_source_updates():
    for source in sources_factory:
        installed_sources[source.ID] = {
            "name": source.NAME,
            "id": source.ID,
            "category": source.CATEGORY,
            "version": version.parse(source.VERSION),
        }

    r = requests.get("https://raw.githubusercontent.com/MangaManagerORG/FMD3-Extensions/repo/extensions.json")
    available_sources = r.json()["sources"]

    for source in installed_sources:
        if source in available_sources:
            if version.parse(available_sources[source]["version"]) > installed_sources[source]["version"]:
                logger.warning(
                    f"New version of {installed_sources[source]['name']} available: {available_sources[source]['version']}")
                get_source(source_id=source)._has_updates = available_sources[source]['version']


def update_source(source_id: str, do_reload_sources=True):
    logger.debug(f"Updating {source_id}")
    if not os.path.exists(SOURCE_PATHS):
        os.makedirs(SOURCE_PATHS)

    # "https://raw.githubusercontent.com/MangaManagerORG/FMD3-Extensions/repo/output"
    r = requests.get(
        "https://raw.githubusercontent.com/MangaManagerORG/FMD3-Extensions/repo/output/sources/" + source_id + ".zip")

    # Save the zip file

    # Extract the contents of the zip file directly from memory
    with zipfile.ZipFile(io.BytesIO(r.content), 'r') as zip_ref:
        top_level_folder = list({item.split('/')[0] + '/' for item in zip_ref.namelist() if '/' in item})[0]
        if os.path.exists(source_path := os.path.join(SOURCE_PATHS, top_level_folder)):
            shutil.rmtree(source_path)
        zip_ref.extractall(SOURCE_PATHS)
    logger.info(f"Successfully updated '{source_id}'")
    if do_reload_sources:
        reload_sources()


def uninstall_source(source_id: str, do_reload_sources=True):
    logger.debug(f"uninstalling source '{source_id}'")
    source = get_source(source_id=source_id)
    sources_factory.remove(source)
    if os.path.exists(source_path := os.path.join(SOURCE_PATHS, source.__class__.__name__)):
        shutil.rmtree(source_path)
    logger.info(f"Successfully uninstalled '{source_id}'")
    if do_reload_sources:
        reload_sources()
