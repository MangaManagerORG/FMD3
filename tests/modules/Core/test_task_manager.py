import time
import unittest
from unittest.mock import patch, MagicMock

from ComicInfo import ComicInfo

from FMD3.core.TaskManager import TaskManager
from tests.TestSource.TestSource import TestSource


class TestTaskManager(unittest.TestCase):
    @patch('FMD3.core.TaskManager.download_series_chapter')
    @patch('FMD3.core.TaskManager.TaskManager.commit')
    def test_queue_items_processed(self,mocked_commit:MagicMock,*_):


        TaskManager().submit_series_chapter(TestSource(), "series_a", TestSource()._debug_get_chapter("series_a","sAcha_1"), "output_file_path",ComicInfo())
        # TaskManager().submit(mocked_commit,
        #     (TestSource, "series_a", TestSource()._debug_get_chapter("series_a", "sAcha_1"), "output_file_path"))

        #Give it time for the thread to finish
        time.sleep(2)
        mocked_commit.assert_called()

    def tearDown(self):
        TaskManager.__instance = None
        TaskManager.__done_list = []



