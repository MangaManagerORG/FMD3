# import userpaths
from pathlib import Path

# is_api = "FMD3_API" in sys.argv[0]
is_development = False
FMD3_PATH = Path(".")
if "FMD3/src/FMD3" in Path(__file__).as_posix():
    is_development = True
    FMD3_PATH = Path(__file__).parent.parent.parent

CONFIG_PATH = Path(FMD3_PATH, "config")
CONFIG_PATH.mkdir(parents=True, exist_ok=True)


DB_PATH = Path(CONFIG_PATH, "FMD3.db")
SETTING_FILE_PATH = Path(CONFIG_PATH, "settings.json")

LOGFILE_PATH = Path(CONFIG_PATH, "logs")
LOGFILE_PATH.mkdir(parents=True, exist_ok=True)


if is_development:
    EXTENSION_PATHS = Path(FMD3_PATH,'../FMD3_Extensions/extensions')
else:
    EXTENSION_PATHS = Path(FMD3_PATH, "extensions")
EXTENSION_PATHS.mkdir(parents=True, exist_ok=True)


SOURCE_PATHS = Path(EXTENSION_PATHS, "sources")
SOURCE_PATHS.mkdir(parents=True, exist_ok=True)

# Make package_ready
with open(Path(SOURCE_PATHS, "__init__.py"), "w") as f:
    f.write("")
