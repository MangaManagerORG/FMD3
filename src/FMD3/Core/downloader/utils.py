import logging
import urllib
from pathlib import Path
from zipfile import ZipFile

from ComicInfo import ComicInfo

from FMD3.Models.Chapter import Chapter
from FMD3.Models.MangaInfo import MangaInfo

NUM_THREADS = 10
DL_FOLDER = "test_download_lib"
from FMD3.Core.database import Session

logger = logging.getLogger(__name__)


def append_cinfo(cbz_path: Path | str, cinfo: ComicInfo):
    with ZipFile(cbz_path, mode="a") as zf:
        zf.writestr(
            "ComicInfo.xml", str(cinfo.to_xml())
        )
