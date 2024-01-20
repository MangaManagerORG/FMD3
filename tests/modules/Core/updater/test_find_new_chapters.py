# def start_fav_scan_schedule():
#     minutes = Settings().get(Updates, Updates.CHECK_NEW_FAV_CHAPTERS_INTERVAL_MINUTES)
#     # minutes = 2
#     if not minutes:
#         print("NO MINUTES DEFINED")
#         return
#     minutes = int(minutes)
#     schedule.every(minutes).seconds.do(new_chapters_finder).run()
import multiprocessing
import os
import threading
import time
import unittest
from unittest.mock import MagicMock

import schedule

from FMD3.Core.database import Base
from FMD3.Core.scheduler import start_fav_scan_schedule, run_scheduler
from FMD3.Core.settings import Settings
from FMD3.Core.settings.Keys import Updates
from FMD3.Core.updater import new_chapters_finder
from FMD3.Sources import ISource, get_source
from FMD3.Core import updater
from FMD3 import Sources
from TestSource import TestSource
from FMD3.Core import database, scheduler

Sources.extesion_factory = [TestSource()]


class TestScheduler(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(database.engine)
        database.Session.rollback()
        # insert_single_chapter in series series_a

        source = get_source("TestSource")
        mi = source.get_info("series_a")
        # first Create series and insert series
        s = database.Series()
        s.title = mi.title
        s.series_id = mi.id
        s.source_id = source.ID
        try:
            database.Session.add(s)
            database.Session.commit()
        except:
            database.Session.rollback()
        # Add the first chapter
        self.sAcha_1 = database.DLDChapters()
        self.sAcha_1.number = 1
        self.sAcha_1.series_id = s.series_id
        self.sAcha_1.chapter_id = "sAcha_1"
        try:
            database.Session.add(self.sAcha_1)
        except:
            database.Session.rollback()

        # Add series b
        mi = source.get_info("series_b")
        s = database.Series()
        s.title = mi.title
        s.series_id = mi.id
        s.source_id = source.ID
        try:
            database.Session.add(s)
            database.Session.commit()
        except:
            database.Session.rollback()

        # add first and only chapter for series
        self.sBcha_1 = database.DLDChapters()
        self.sBcha_1.number = 1
        self.sBcha_1.series_id = s.series_id
        self.sBcha_1.chapter_id = "sBcha_1"
        try:
            database.Session.add(self.sBcha_1)
        except:
            database.Session.rollback()
    def test_find_new_chapters(self):
        """
        Simulates the flow where updater filters the chapters that are not yet in the database and passes the list to the task manager to download
        Returns:

        """
        def sd_effect (source, series, chapters, *args,**kwargs):
            self.assertNotIn(self.sAcha_1, chapters)
        mock_make_download_task_missing_chapters = MagicMock()
        mock_make_download_task_missing_chapters.side_effect = sd_effect
        updater.make_download_task_missing_chapters = mock_make_download_task_missing_chapters

        new_chapters_finder()
    def test_find_new_chapters_should_not_detect_new_chapters(self):
        """
        Simulates the flow where updater filters the chapters that are not yet in the database and passes the list to the task manager to download
        Returns:

        """
        # Find chapters
        new_chapters_finder()

        # Find again
        new_chapters_finder()

        def sd_effect (source, series, chapters, *args,**kwargs):
            self.assertNotIn(self.sBcha_1, chapters)
        mock_make_download_task_missing_chapters = MagicMock()
        mock_make_download_task_missing_chapters.side_effect = sd_effect
        updater.make_download_task_missing_chapters = mock_make_download_task_missing_chapters




        mock_make_download_task_missing_chapters = MagicMock()
        updater.make_download_task_missing_chapters = mock_make_download_task_missing_chapters

        mock_make_download_task_missing_chapters.assert_not_called()

# def test_scheduler(self):
#     called_counter = 0

# mock_chapter = MagicMock()
# mock_chapter.side_effect = lambda x:x[0]+1
# # set it to run every 3 seconds
# Settings().set(Updates, Updates.CHECK_NEW_FAV_CHAPTERS_INTERVAL_MINUTES,4)
# scheduler.new_chapters_finder = mock_chapter
#
# scheduler_thread = threading.Thread(target=run_scheduler,args=(called_counter,))
# scheduler_thread.start()
#
# timeout_start = time.time()
# while called_counter< 2:
#     if time.time() - timeout_start > 10:
#         ...
#         # scheduler_thread.terminate()
# self.assertEqual(mock_chapter.call_count,2)
# return