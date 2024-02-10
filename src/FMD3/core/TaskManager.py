import logging
import threading

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures.process import BrokenProcessPool

from FMD3.core import database
from FMD3.core.database import DLDChapters
from FMD3.core.database.predefined import chapter_exists
from FMD3.core.downloader import download_series_chapter


def exception_handler(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception:
        logging.getLogger().exception(f"Exception in thread {threading.current_thread().name}")


class TaskManager:
    __instance = None
    __TPE = None
    __log = logging.getLogger()

    def __new__(cls):
        if TaskManager.__instance is None:
            TaskManager.__instance = object.__new__(cls)
            # TaskManager.__TPE = ThreadPoolExecutor(max_workers=10)
            TaskManager.__TPE = ProcessPoolExecutor(max_workers=10)
            TaskManager.active_tasks = set()
        return TaskManager.__instance

    def __init__(self):
        self.__done_list = []

    def submit(self, func, *args, **kwargs):
        task = self.__TPE.submit(exception_handler, func, *args, **kwargs)
        task.add_done_callback(self.commit)

    def commit(self, future):
        try:
            series_id, chapter_id, status = future.result()
        except BrokenProcessPool:
            # Main process that excepted raised exceptions.
            # These are just telling one process exited thus provides no info
            pass
        status: DLDCS
        logging.getLogger(__name__).info("Marking chapter as done")
        database.Session().query(database.DLDChapters).filter(DLDChapters.chapter_id == chapter_id,
                                                              DLDChapters.series_id == series_id).one().status = status.value
        database.Session().commit()
        self.active_tasks.remove(f"{series_id}/{chapter_id}")
        ...

    def submit_series_chapter(self, source, series_id, chapter, path, cinfo, *args, **kwargs):
        # Check chapter is not fully downloaded
        # Check if chapter is not in active tasks
        if f"{series_id}/{chapter.chapter_id}" not in self.active_tasks:
            if not chapter_exists(series_id, chapter.chapter_id):
                ret = database.DLDChapters()
                ret.chapter_id = chapter.chapter_id
                ret.series_id = series_id
                ret.number = chapter.number
                ret.title = chapter.title
                ret.volume = chapter.volume
                ret.status = 2
                ret.path = str(path)
                database.Session().add(ret)
                database.Session().commit()
            elif dbchapter := database.Session().query(DLDChapters).filter_by(series_id=series_id,
                                                                      chapter_id=chapter.chapter_id).one():
                if dbchapter:
                    chapter_status = DLDCS(dbchapter.status)
                    if chapter_status in [DLDCS.DOWNLOADED, DLDCS.SKIPPED]:
                        # Assume chapter is already downloaded, skipped or failed
                        logging.getLogger(__name__).debug(f"Aborting task -> '{chapter_status}' chapter id: '{chapter.chapter_id}'")
                        return

            logging.getLogger(__name__).info(f"Adding download task for {series_id} . Ch.{chapter.number}")
            self.active_tasks.add(f"{series_id}/{chapter.chapter_id}")
            future = self.__TPE.submit(exception_handler, download_series_chapter, source, series_id, chapter, path,
                                       cinfo, *args, **kwargs)
            future.add_done_callback(self.commit)
        else:
            logging.getLogger(__name__).info(
                f"Chapter id {chapter.chapter_id}, number {chapter.number} is registered in db. Skipping")
            ...
