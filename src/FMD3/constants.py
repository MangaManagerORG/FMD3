import userpaths
from pathlib import Path

CONFIG_PATH = Path(userpaths.get_local_appdata(), "FMD3", "config")
CONFIG_PATH.mkdir(parents=True, exist_ok=True)


LOGFILE_PATH = Path(userpaths.get_local_appdata(), "FMD3", "config", "logs")
LOGFILE_PATH.mkdir(parents=True, exist_ok=True)


DB_PATH = Path(userpaths.get_local_appdata(), "FMD3", "config", "FMD3.db")


SETTING_FILE_PATH = Path(userpaths.get_local_appdata(), "FMD3", "config", "settings.json")

EXTENSION_PATHS = Path(userpaths.get_local_appdata(), "FMD3", "extensions")
EXTENSION_PATHS.mkdir(parents=True, exist_ok=True)

SOURCE_PATHS = Path(userpaths.get_local_appdata(), "FMD3", "extensions", "sources")
SOURCE_PATHS.mkdir(parents=True, exist_ok=True)
# Make package_ready
with open(Path(SOURCE_PATHS, "__init__.py"), "w") as f:
    f.write("")
