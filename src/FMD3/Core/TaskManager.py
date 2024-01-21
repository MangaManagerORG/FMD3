import logging
import threading

from concurrent.futures import ThreadPoolExecutor

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
            TaskManager.__TPE = ThreadPoolExecutor(max_workers=10)
        return TaskManager.__instance

    def __init__(self):
        self.__done_list = []

    def submit(self, func, *args, **kwargs):
        task = self.__TPE.submit(exception_handler, func, *args, **kwargs)
        task.add_done_callback(self.commit)

    def commit(self, future):
        # if a:=future.result():
        #     try:
        #         Session().add(a)
        #         Session().commit()
        #     except:
        #         Session.rollback()
        #         logging.getLogger().exception("Error submitting chapter")
        #         raise
        # logging.error("task did not return chapter")
        ...

    def submit_series_chapter(self, *args, **kwargs):
        self.__done_list.append(self.__TPE.submit(exception_handler, download_series_chapter, *args, **kwargs))
