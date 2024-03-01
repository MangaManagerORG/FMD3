import logging
import os
from pathlib import Path
from zipfile import ZipFile
from ComicInfo import ComicInfo

from FMD3.models.chapter import Chapter

NUM_THREADS = 10
DL_FOLDER = "test_download_lib"

logger = logging.getLogger(__name__)


def append_cinfo(cbz_path: Path | str, cinfo: ComicInfo):
    with ZipFile(cbz_path, mode="a") as zf:
        zf.writestr(
            "ComicInfo.xml", str(cinfo.to_xml())
        )


def analyze_archive(output_file_path, series_id, chapter: Chapter) -> bool:
    """
        Analyzes an archive file to determine if it exists and has the correct number of files.

        Parameters:
        - output_file_path (str): The path to the archive file to be analyzed.
        - series_id (str): The identifier of the series.
        - chapter (Chapter): The Chapter object representing the chapter information.

        Returns:
        - bool: True if the file exists and has the correct number of files, indicating that it has already been downloaded;
                False otherwise, indicating that the file needs to be processed.

        The function checks if the specified archive file exists. If it exists, it reads the contents of the archive to
        determine the number of image files (".webp", ".jpg", ".png") and chapter information files (".xml"). If the count
        matches the expected number of pages in the chapter plus one (for the chapter information file), it logs a warning
        message indicating that the file is already downloaded and returns True. Otherwise, it returns False, indicating
        that the file needs to be processed further.
        """
    if Path(output_file_path).exists():
        logger.trace("Analyzing file: {}".format(output_file_path))
        try:
            with ZipFile(Path(output_file_path), "r") as zf:
                n_images_and_cinfo = len([file for file in zf.namelist() if
                                          os.path.splitext(file)[1].lower() in [".webp", ".jpg", ".png", ".xml"]])
                if n_images_and_cinfo == chapter.pages + 1:
                    logger.warning(
                        f"File '{output_file_path}' - series '{series_id}' chapter number '{chapter.number}' chapter id '{chapter.chapter_id}' is apparently already downloaded. Skipping with status 4")
                    return True
        except Exception:
            logger.exception("Unhandled error analyzing file")
            return False
    return False