import unittest

import sqlalchemy

from FMD3.Core.database import Session, DLDChapters
from FMD3.Core.database.predefined import chapter_exists


class TestPredefined(unittest.TestCase):
    def test_predefined(self):

        chapter = DLDChapters()
        chapter.title = "Title"
        chapter.chapter_id = "cha1"
        chapter.series_id = "ser1"
        try:
            Session().add(chapter)
            Session.commit()
        except Exception:
            Session().rollback()
        print("sdasds")
        self.assertTrue(chapter_exists("ser1","cha1"))