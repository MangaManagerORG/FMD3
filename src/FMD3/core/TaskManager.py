import logging
import threading

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from concurrent.futures.process import BrokenProcessPool

from FMD3.core import database
from FMD3.core.database import DLDChapters
from FMD3.core.database.predefined import chapter_exists
from FMD3.core.downloader.processing import convert_and_zip
from FMD3.core.downloader.utils import analyze_archive
from FMD3.models.ddl_chapter_status import DLDChaptersStatus as DDLCS
from FMD3.models.download_task import DownloadTask
from FMD3.core.downloader.downloader import download_images_for_chapter

logger = logging.getLogger(__name__)
print_once_process_exception = False
lock = threading.Lock()

class TaskManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            TaskManager.__instance = object.__new__(cls)
            TaskManager.__instance.__DPE = ThreadPoolExecutor(max_workers=5)  # Download Pool executro
            TaskManager.__instance.__PPE = ProcessPoolExecutor()
            TaskManager.__instance.active_tasks = set()
            TaskManager.__instance.tasks_statuses = {}
        return cls.__instance

    def _pre_update_status(self, task_id, func, *args):
        with lock:
            self.tasks_statuses[task_id] = "downloading"
        return func(*args)


    def submit_series_chapter(self, source, series_id, chapter, path, cinfo, manual_download, *args, **kwargs):
        """
        Submits a chapter for download
        Args:
            source:
            series_id:
            chapter:
            path:
            cinfo:
            manual_download: whether the download was triggered by the user if True else triggered by the updater
            *args:
            **kwargs:

        Returns:

        """
        task_id = f"{series_id}/{chapter.chapter_id}"
        # Check chapter is not fully downloaded
        # Check if chapter is not in active tasks
        if task_id not in self.active_tasks:
            if not chapter_exists(series_id, chapter.chapter_id):
                ret = database.DLDChapters()
                ret.chapter_id = chapter.chapter_id
                ret.series_id = series_id
                ret.number = chapter.number
                ret.title = chapter.title
                ret.volume = chapter.volume
                ret.status = (DDLCS.ADDED_TO_QUEUE_USER if manual_download else DDLCS.ADDED_TO_QUEUE_SCANNER).value
                ret.path = str(path)
                database.Session().add(ret)
                database.Session().commit()
        elif dbchapter := database.Session().query(DLDChapters).filter_by(series_id=series_id,
                                                                          chapter_id=chapter.chapter_id).one():
            if dbchapter:
                chapter_status = DDLCS(dbchapter.status)
                if chapter_status in [DDLCS.DOWNLOADED, DDLCS.SKIPPED]:
                    # Assume chapter is already downloaded, skipped or failed
                    logging.getLogger(__name__).debug(
                        f"Aborting task -> '{chapter_status}' chapter id: '{chapter.chapter_id}'")
                    return

        logging.getLogger(__name__).info(f"Adding download task for {series_id} . Ch.{chapter.number}")
        self.active_tasks.add(task_id)
        self.tasks_statuses[task_id] = "Waiting"
        dl_obj = DownloadTask(source, series_id, chapter, path, cinfo)
        if analyze_archive(dl_obj.output_path, series_id, chapter):
            self.on_process_done(dl_obj)
            return

        thread_future = self.__DPE.submit(self._pre_update_status,task_id, download_images_for_chapter, dl_obj)
        thread_future.add_done_callback(lambda future: self.on_thread_done(thread_future))

    def on_thread_done(self, thread_future):
        # Callback function called when the thread task is done

        thread_result: DownloadTask = thread_future.result()

        logger.info(f"Downloading complete for {thread_result.chapter}")
        process_future = self.__PPE.submit(convert_and_zip, thread_result)
        process_future.add_done_callback(self.pre_on_process_done)
        self.tasks_statuses[f"{thread_result.series_id}/{thread_result.chapter.chapter_id}"] = "compressing"

    def pre_on_process_done(self,future):
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
        return self.on_process_done(task)

    def on_process_done(self, task):

        if task.status == DDLCS.DOWNLOADED:
            logger.info(f"Processing done for {task.chapter}")
        if task.status == DDLCS.SKIPPED:
            logger.warning(f"Processing skipped for {task.chapter}")
        else:
            logger.error(f"Process failed for {task.chapter}")

        database.Session().query(database.DLDChapters).filter(DLDChapters.chapter_id == task.chapter.chapter_id,
                                                              DLDChapters.series_id == task.series_id).one().status = task.status.value
        database.Session().commit()
        self.active_tasks.remove(f"{task.series_id}/{task.chapter.chapter_id}")
        del self.tasks_statuses[f"{task.series_id}/{task.chapter.chapter_id}"]
