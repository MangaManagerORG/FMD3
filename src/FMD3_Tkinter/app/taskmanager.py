import logging
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger()


def try_func(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except:
        logger.exception("Exception")


class TaskManager:
    def __init__(self):
        self.__DPE = ThreadPoolExecutor(max_workers=2)
        self.__instance = self
        self.active_tasks = set()

    def submit(self, func, callback, *args, **kwargs):
        thread_future = self.__DPE.submit(try_func, func, *args, **kwargs)
        if callback is not None:
            thread_future.add_done_callback(lambda future=thread_future: callback(future.result()))
        else:
            thread_future.result()
