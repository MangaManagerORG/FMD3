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
from unittest.mock import MagicMock, patch

import schedule
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from FMD3.core.database import Base, Series
from FMD3.core.updater import new_chapters_finder, create_download_task
from FMD3.sources import ISource, get_source
from FMD3.core import updater, TaskManager
from FMD3 import sources
from tests.TestSource.TestSource import TestSource
from FMD3.core import database, scheduler
sources.sources_factory = [TestSource()]

database.engine = create_engine('sqlite:///', isolation_level="SERIALIZABLE")

session_factory = sessionmaker(bind=database.engine)
database.Session = scoped_session(session_factory)
from FMD3.core.database import predefined
predefined.Session = database.Session
from FMD3.core.database import models
models.Session = database.Session
get_scoped_session = None

class DbSetup(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(database.engine)
        database.Session.rollback()
        # insert_single_chapter in series series_a

        source = get_source("TestSource")
        mi = source.get_info("series_a")
        # first Create series and insert series
        self.series_a = s = database.Series()
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
        self.series_b = s = database.Series()
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
            database.Session.commit()
        except:
            database.Session.rollback()
class TestFindNewChapters(DbSetup):

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
        mock_make_download_task_missing_chapters.assert_not_called()

class TestMakeDownloadTask(DbSetup):
    @unittest.skip("need to be rethinked")
    def test_all_tasks_created_for_chapter(self):

        mock = TaskManager.TaskManager.submit_series_chapter = MagicMock()
        chapters = TestSource().get_chapters("series_a")
        create_download_task(TestSource(), self.series_a, chapters)

        # assert callcount to 1 as chapter 1 is added to downloads in setup
        self.assertEqual(1, mock.call_count)

    @unittest.skip("No longer applicable")
    def test_all_tasks_created_for_chapter_series_b_should_not_create(self):
        """
        Asserts that no chapters are ready to download since series b only has one chapter and is downloaded (made in setup)
        Returns:
        """
        mock = TaskManager.TaskManager.submit_series_chapter = MagicMock()
        chapters = TestSource().get_chapters("series_b")
        make_download_task_missing_chapters(TestSource(), self.series_b, chapters)

        mock.assert_not_called()
