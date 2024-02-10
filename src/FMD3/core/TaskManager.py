import logging
import threading

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from concurrent.futures.process import BrokenProcessPool

from FMD3.core import database
from FMD3.core.database import DLDChapters
from FMD3.core.database.predefined import chapter_exists
from FMD3.core.downloader.processing import convert_and_zip
from FMD3.models.ddl_chapter_status import DLDChaptersStatus
from FMD3.models.download_task import DownloadTask
from FMD3.core.downloader.downloader import download_images_for_chapter

logger = logging.getLogger(__name__)
print_once_process_exception = False


class TaskManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            TaskManager.__instance = object.__new__(cls)
            TaskManager.__instance.__DPE = ThreadPoolExecutor(max_workers=5)  # Download Pool executro
            TaskManager.__instance.__PPE = ProcessPoolExecutor()
            TaskManager.__instance.active_tasks = set()
        return cls.__instance

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
                chapter_status = DLDChaptersStatus(dbchapter.status)
                if chapter_status in [DLDChaptersStatus.DOWNLOADED, DLDChaptersStatus.SKIPPED]:
                    # Assume chapter is already downloaded, skipped or failed
                    logging.getLogger(__name__).debug(
                        f"Aborting task -> '{chapter_status}' chapter id: '{chapter.chapter_id}'")
                    return

        logging.getLogger(__name__).info(f"Adding download task for {series_id} . Ch.{chapter.number}")
        self.active_tasks.add(f"{series_id}/{chapter.chapter_id}")

        dl_obj = DownloadTask(source, series_id, chapter, path, cinfo, *args, **kwargs)

        thread_future = self.__DPE.submit(download_images_for_chapter, dl_obj)
        thread_future.add_done_callback(lambda future: self.on_thread_done(thread_future))

    def on_thread_done(self, thread_future):
        # Callback function called when the thread task is done

        thread_result: DownloadTask = thread_future.result()

        logger.info(f"Downloading complete for {thread_result.chapter}")
        process_future = self.__PPE.submit(convert_and_zip, thread_result)
        process_future.add_done_callback(self.on_process_done)

    def on_process_done(self, future):
        # def commit(self, future):
        try:
            task: DownloadTask = future.result()
        except BrokenProcessPool:
            global print_once_process_exception
            # Main process that excepted raised exceptions.
            # These are just telling one process exited thus provides no info
            if not print_once_process_exception:
                logger.exception(f"Unhandled exception")
                print_once_process_exception = True
            print("")
            return
        except:
            logger.exception(f"Unhandled exception")

        if task.status == DLDChaptersStatus.DOWNLOADED:
            logger.info(f"Processing done for {task.chapter}")
        else:
            logger.error(f"Process failed for {task.chapter}")

        database.Session().query(database.DLDChapters).filter(DLDChapters.chapter_id == task.chapter.chapter_id,
                                                              DLDChapters.series_id == task.series_id).one().status = task.status.value
        database.Session().commit()
        self.active_tasks.remove(f"{task.series_id}/{task.chapter.chapter_id}")
