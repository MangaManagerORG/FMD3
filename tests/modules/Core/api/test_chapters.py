import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from FMD3.api.api import Api
from FMD3.core.database import Series, DLDChapters
from FMD3.models.ddl_chapter_status import DLDChaptersStatus
from tests.TestSource.TestSource import TestSource
from tests.dbutils import make_session

source = TestSource()
s = Series()
s.title = "Series A"
s.series_id = "series_a"
s.source_id = source.ID
s.enabled = True

sb = Series()
sb.title = "Series A"
sb.series_id = "series_a"
sb.source_id = source.ID
sb.enabled = True


@patch('FMD3.api.api.Api.get_source',return_value=source)
@patch('FMD3.api.routes.chapters.db.Session', new_callable=make_session)
class TestChapters(unittest.TestCase):
    @patch("FMD3.api.routes.chapters.sup_get_source", return_value=source)
    @patch("FMD3.api.routes.chapters.create_download_task")
    def test_download_chapters(self,create_download_task: MagicMock,__, mock_session,*_):
        mock_session().add(s)
        mock_session().commit()
        chapters = source.get_chapters(s.series_id)
        chapter_ids = [chapter.chapter_id for chapter in chapters]
        Api.download_chapters(
            source_id=s.source_id,
            series_id=s.series_id,
            chapter_ids=chapter_ids,
            output_path=""
        )

        create_download_task.assert_called_with(source, s, source.get_queried_chapters(s.series_id, chapter_ids))
        print("chapters")

    def test_get_soure_chapters(self, *args, **kwargs):
        a = Api.get_source_chapters(s.source_id, s.series_id)

        chapters = source.get_chapters(s.series_id)
        for a in a:
            self.assertTrue(list(filter(lambda x: x.chapter_id == a["chapter_id"],chapters)))

    def test_get_chapters(self, session, *args, **kwargs):

        c = DLDChapters()
        c.status = DLDChaptersStatus.DOWNLOADED
        c.series_id = sb.series_id
        c.chapter_id = "sBcha_1"
        c.number = 5
        c.volume = 1
        c.added_at = datetime.now() - timedelta(hours=3)

        session().add(c)

        a = Api.get_chapters(sb.series_id)

        for chapter in a:
            self.assertEqual("sBcha_1",chapter["chapter_id"])

        print("")