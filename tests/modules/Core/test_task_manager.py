import time
import unittest
from unittest.mock import patch, MagicMock

from ComicInfo import ComicInfo

from FMD3.core.TaskManager import TaskManager
from tests.TestSource.TestSource import TestSource
from FMD3.models.download_task import DownloadTask


class TestTaskManager(unittest.TestCase):
    @patch('FMD3.core.TaskManager.download_images_for_chapter',
           return_value=DownloadTask(TestSource(),
                                     series_id="series_a",
                                     chapter=TestSource()._debug_get_chapter(
                                         series_id="series_a",
                                         chapter_id="sAcha_1"),
                                     output_path="output_file_path",
                                     cinfo=ComicInfo()))
    @patch('FMD3.core.TaskManager.TaskManager.on_process_done')
    def test_queue_items_processed(self, on_process_done: MagicMock, *_):
        TaskManager().submit_series_chapter(
            source=TestSource(),
            series_id="series_a",
            chapter=TestSource()._debug_get_chapter("series_a", "sAcha_1"),
            path="output_file_path",
            cinfo=ComicInfo())
        # TaskManager().submit(mocked_commit,
        #     (TestSource, "series_a", TestSource()._debug_get_chapter("series_a", "sAcha_1"), "output_file_path"))

        # Give it time for the thread to finish
        time.sleep(2)
        on_process_done.assert_called()

    def tearDown(self):
        TaskManager.__instance = None
        TaskManager.__done_list = []
