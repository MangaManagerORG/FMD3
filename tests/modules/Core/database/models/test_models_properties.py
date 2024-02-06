import unittest

from FMD3.core.database import DLDChapters
from tests.TestSource.TestSource import TestSource

class TestModelsProperties(unittest.TestCase):
    def test_DDL_creates_valid_chapter(self):

        chapter = DLDChapters.from_chapter(TestSource().get_chapters("series_a")[0],series_id="series_a")
        self.assertEqual(chapter.chapter_id,"sAcha_1")