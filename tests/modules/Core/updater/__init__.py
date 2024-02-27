import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from FMD3.core.database import Series, DLDChapters, SeriesStatus
from FMD3.models.ddl_chapter_status import DLDChaptersStatus
from FMD3.core.updater import create_download_task, scan_hanging_tasks, scan_new_chapters, new_chapters_finder
from tests.TestSource.TestSource import TestSource
from tests.dbutils import make_session


@patch("FMD3.core.updater.get_source_by_id", return_value=TestSource())
@patch("FMD3.core.updater.create_download_task")
class TestScanHangingTasks(unittest.TestCase):
    @patch("FMD3.core.updater.Session", new_callable=make_session())
    def test_hanging_chapter_expired(self, mock_Session, mock_create_downloads_task: MagicMock, *_):
        source = TestSource()
        s = Series()
        s.title = "Series A"
        s.series_id = "series_a"
        s.source_id = source.ID
        mock_Session.add(s)
        mock_Session.commit()

        # create a hanging task
        c = DLDChapters()
        c.status = DLDChaptersStatus.ADDED_TO_QUEUE_SCANNER.value
        c.series_id = s.series_id
        c.chapter_id = "sAcha_1"
        c.number = 5
        c.volume = 1
        c.downloaded_at = datetime.now() - timedelta(hours=3)
        mock_Session.add(c)
        mock_Session.commit()

        scan_hanging_tasks()
        mock_create_downloads_task.assert_called()
        print("sdas")


@patch("FMD3.core.updater.get_sources_list", return_value=[TestSource()])
@patch("FMD3.core.updater.create_download_task")
class TestScanNewChapters(unittest.TestCase):
    @patch("FMD3.core.updater.Session", new_callable=make_session)
    def test_scan_new_chapters(self, mock_session, mock_create_download_task: MagicMock, *_):

        # Create and add series
        source = TestSource()
        s = Series()
        s.title = "Series A"
        s.series_id = "series_a"
        s.source_id = source.ID
        s.enabled = True
        s.favourited = True
        mock_session().add(s)
        mock_session().commit()

        scan_new_chapters()
        mock_create_download_task.assert_called()


@patch("FMD3.core.updater.Session")
class TestCreateDownloadTask(unittest.TestCase):

    @patch("FMD3.core.updater.TaskManager.submit_series_chapter")
    def test_create_download_task(self, mock_submit_series_chapter: MagicMock, mock_Session):
        mock_Session = make_session()

        source = TestSource()
        s = Series()
        s.title = "Series A"
        s.series_id = "series_a"
        s.source_id = source.ID
        s.enabled = True
        s.save_to = "Series a Folder"
        ch_list = [source._debug_get_chapter(s.series_id, "sAcha_1"), source._debug_get_chapter(s.series_id, "sAcha_2")]
        create_download_task(source, s, ch_list)
        mock_submit_series_chapter.assert_called()


# This one for shake of completness in coverage

@patch("FMD3.core.updater.get_sources_list", return_value=[TestSource()])
@patch("FMD3.core.updater.Session", new_callable=make_session)
@patch("FMD3.core.updater.TaskManager")
class TestNewChapterFinder(unittest.TestCase):
    @patch("FMD3.core.updater.create_download_task")
    def test_new_chapters_finder(self,mock_download_task, mock_task_mngr: MagicMock, mock_session, *_):
        mock_task_mngr().submit_series_chapter = MagicMock()
        source = TestSource()
        s = Series()
        s.title = "Series A"
        s.series_id = "series_a"
        s.source_id = source.ID
        s.enabled = True
        s.favourited = True
        s.save_to = "Series a Folder"
        mock_session().add(s)
        mock_session().commit()
        # ch_list = [source._debug_get_chapter(s.series_id, "sAcha_1"), source._debug_get_chapter(s.series_id, "sAcha_2")]

        new_chapters_finder()
        # mock_download_task
        mock_download_task.assert_called()
        # mock_task_mngr().submit_series_chapter.assert_called()
    @patch("FMD3.core.updater.create_download_task")
    @patch("FMD3.core.updater.max_chapter_number",return_value=1)
    @patch("FMD3.core.updater.__no_new_chapters")
    def test_new_chapters_finder_should_have_no_more_chapters(self, mock_no_new_chapters: MagicMock, mock_max_ch_num, mock_create_download_task:MagicMock ,mock_submit_series_chapter: MagicMock, mock_session, *_):
        source = TestSource()
        s = Series()
        s.title = "Series B"
        s.series_id = "series_b"
        s.source_id = source.ID
        s.enabled = True
        s.save_to = "Series b Folder"
        mock_session().add(s)
        mock_session().commit()
        # Make chapter as if it were downloaded
        c = DLDChapters()
        c.status = DLDChaptersStatus.DOWNLOADED.value
        c.series_id = s.series_id
        c.chapter_id = "sBcha_1"
        c.number = 5
        c.volume = 1
        c.downloaded_at = datetime.now() - timedelta(hours=3)
        mock_session.add(c)
        mock_session.commit()

        # ch_list = [source._debug_get_chapter(s.series_id, "sAcha_1"), source._debug_get_chapter(s.series_id, "sAcha_2")]

        new_chapters_finder()
        # Assert not called. new logic determines that the chapter max chapter is the same as source max chapter thus not needing one extra call
        mock_create_download_task.assert_not_called()
        # mock_submit_series_chapter.assert_called()

    @patch("FMD3.core.updater.create_download_task")
    @patch("FMD3.core.updater.max_chapter_number",return_value=1)
    @patch("FMD3.core.updater.__no_new_chapters")
    def test_new_chapters_finder_should_skip_fully_downloaded_series(self,mock_no_new_chapters:MagicMock,mock_max_ch_num, mock_create_download_task:MagicMock ,mock_submit_series_chapter: MagicMock, mock_session, *_):
        source = TestSource()
        s = Series()
        s.title = "Series B"
        s.series_id = "series_b"
        s.source_id = source.ID
        s.enabled = True
        s.status = SeriesStatus.FULLY_DOWNLOADED.value
        s.save_to = "Series b Folder"
        mock_session().add(s)
        mock_session().commit()
        # Make chapter as if it were downloaded
        c = DLDChapters()
        c.status = DLDChaptersStatus.DOWNLOADED.value
        c.series_id = s.series_id
        c.chapter_id = "sBcha_1"
        c.number = 5
        c.volume = 1
        c.downloaded_at = datetime.now() - timedelta(hours=3)
        mock_session.add(c)
        mock_session.commit()

        # ch_list = [source._debug_get_chapter(s.series_id, "sAcha_1"), source._debug_get_chapter(s.series_id, "sAcha_2")]

        new_chapters_finder()
        # Assert not called. new logic determines that the chapter max chapter is the same as source max chapter thus not needing one extra call
        mock_create_download_task.assert_not_called()
        # mock_submit_series_chapter.assert_called()