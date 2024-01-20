import logging
import queue
from concurrent.futures import ThreadPoolExecutor

from FMD3.Core.downloader import download_series_chapter


class TaskManager:
    __instance = None
    # __TPE =
    __log = logging.getLogger()
    __done_list: list = []

    def __new__(cls):
        if TaskManager.__instance is None:
            TaskManager.__instance = object.__new__(cls)
            TaskManager.__TPE = ThreadPoolExecutor(max_workers=3)
            TaskManager.__done_queue = queue.Queue()
        return TaskManager.__instance

    def submit(self, func, *args, **kwargs):
        self.__done_list.append(self.__TPE.submit(func, args, kwargs))

    def submit_series_chapter(self, *args, **kwargs):
        self.__done_list.append(self.__TPE.submit(download_series_chapter, *args, **kwargs))