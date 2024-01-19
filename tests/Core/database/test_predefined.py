import unittest

from FMD3.Core.database import Session, DLDChapters
from FMD3.Core.database.predefined import chapter_exists


class TestPredefined(unittest.TestCase):
    def test_predefined(self):

        session = Session()
        chapter = DLDChapters()
        chapter.title = "Title"
        chapter.chapter_id = "cha1"
        chapter.series_id = "ser1"

        session.add(chapter)

        self.assertTrue(chapter_exists("ser1","cha1"))