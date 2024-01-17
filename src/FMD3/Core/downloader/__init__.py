import asyncio
import logging
import os
from pathlib import Path
from queue import Queue
from threading import Thread
import urllib.request

from FMD3.Extensions import IExtension

NUM_THREADS = 3
DL_FOLDER = "test_download_lib"


class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    total_file_count = 0
    files_processed_count = 0
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(worker=self,*args, **kargs)
                self.files_processed_count +=1
            except Exception as e:
                logging.getLogger().exception("Error running task")
            finally:
                self.tasks.task_done()

    def percent_done(self):
        """Gets the current percent done for the thread."""
        return float(self.files_processed_count) / \
            float(self.total_file_count) \
            * 100.0

    def get_progress(self):
        """Can be called at any time before, during or after thread
        execution, to get current progress."""
        return '%d files (%.2f%%)' % (self.files_processed_count,
                                      self.percent_done())


class ThreadPool:
    """Pool of threads consuming tasks from a queue"""

    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """Add a task to the queue"""
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()
def download_image(img_url, folder, filename):
    try:
        logging.getLogger().info(f"Downloading from '{img_url}'")
        urllib.request.urlretrieve(img_url, Path(folder,filename))
    except:
        logging.getLogger().exception("Exception downloading")

def download_chapter(module: IExtension, chapters_urls: list[str],worker=None):
    worker.total_file_count = len(chapters_urls)
    for i, ch_url in enumerate(chapters_urls):
        ch_url = chapters_urls[0]
        path = Path(f"{os.getcwd()}/{DL_FOLDER}/{i}")
        path.mkdir(exist_ok=True, parents=True)

        files = module.on_get_page_number(ch_url)
        for img_url, img_filename in files:
            path = Path(f"{os.getcwd()}/{DL_FOLDER}/1")
            download_image(img_url, str(path), img_filename)

def download(extension_downloads: list[tuple[IExtension, list[str]]]):
    # module: IExtension, url):
    """Here goes the job to be added into the thread pool"""
    for module, chapters  in extension_downloads:
        pool.add_task(download_chapter, module, chapters)
    print("")
    pool.wait_completion()



"""Defining thread pool"""

pool = ThreadPool(NUM_THREADS)

# """Workflow - TODO"""
# pool.add_task(job,parama_a)
# pool.wait_completion()
