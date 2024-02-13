import userpaths
from pathlib import Path

print(__file__)

import sys

# is_api = "FMD3_API" in sys.argv[0]

FMD3_PATH = Path(".")


# CONFIG_PATH = Path("config")  # TODO("Change this back") #
CONFIG_PATH = Path(FMD3_PATH, "config")
CONFIG_PATH.mkdir(parents=True, exist_ok=True)


DB_PATH = Path(CONFIG_PATH, "FMD3.db")
SETTING_FILE_PATH = Path(CONFIG_PATH, "settings.json")

LOGFILE_PATH = Path(CONFIG_PATH, "logs")
LOGFILE_PATH.mkdir(parents=True, exist_ok=True)


# EXTENSION_PATHS = Path('./../FMD3_Extensions/extensions')  # TODO("Change this back")) #
EXTENSION_PATHS = Path(FMD3_PATH, "extensions")
EXTENSION_PATHS.mkdir(parents=True, exist_ok=True)


SOURCE_PATHS = Path(EXTENSION_PATHS, "sources")
SOURCE_PATHS.mkdir(parents=True, exist_ok=True)

# Make package_ready
with open(Path(SOURCE_PATHS, "__init__.py"), "w") as f:
    f.write("")
