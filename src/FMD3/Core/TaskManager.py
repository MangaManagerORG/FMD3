import logging
import threading

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from FMD3.Core import database
from FMD3.Core.database import DLDChapters
from FMD3.Core.database.predefined import chapter_exists
from FMD3.Core.downloader import download_series_chapter


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
        return TaskManager.__instance

    def __init__(self):
        self.__done_list = []
        self.active_tasks = set()

    def submit(self, func, *args, **kwargs):
        task = self.__TPE.submit(exception_handler, func, *args, **kwargs)
        task.add_done_callback(self.commit)

    def commit(self, future):
        series_id, chapter_id, status = future.result()
        logging.getLogger(__name__).info("Marking chapter as done")
        database.Session().query(database.DLDChapters).filter(DLDChapters.chapter_id == chapter_id,
                                                              DLDChapters.series_id == series_id).one().status = status
        database.Session().commit()
        self.active_tasks.remove(f"{series_id}/{chapter_id}")
        ...

    def submit_series_chapter(self, source, series_id, chapter, path, cinfo, *args, **kwargs):

        ret = database.DLDChapters()
        ret.chapter_id = chapter.id
        ret.series_id = series_id
        ret.number = chapter.number
        ret.title = chapter.title
        ret.volume = chapter.volume
        ret.status = 2
        ret.path = str(path)
        # Check chapter is not fully downloaded
        # Check if chapter is not in active tasks
        if not chapter_exists(series_id,chapter.id) and f"{series_id}/{chapter.id}" not in self.active_tasks:

            logging.getLogger(__name__).info(f"Adding download task for {series_id} . Ch.{chapter.number}")
            database.Session().add(ret)
            database.Session().commit()
            self.active_tasks.add(f"{series_id}/{chapter.id}")
            future = self.__TPE.submit(exception_handler, download_series_chapter, source, series_id, chapter, path,
                                       cinfo, *args, **kwargs)
            future.add_done_callback(self.commit)
        else:
            logging.getLogger(__name__).info(
                f"Chapter id {chapter.id}, number {chapter.number} is registered in db. Skipping")
            ...
