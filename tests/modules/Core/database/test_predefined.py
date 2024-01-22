import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from FMD3.Core import database
from FMD3.Core.database import DLDChapters, Base
from FMD3.Core.database.predefined import chapter_exists


database.engine = create_engine('sqlite:///', isolation_level="SERIALIZABLE")

session_factory = sessionmaker(bind=database.engine)
database.Session = scoped_session(session_factory)
Base.metadata.create_all(database.engine)

class TestPredefined(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(database.engine)
    def test_predefined(self):

        chapter = DLDChapters()
        chapter.title = "Title"
        chapter.chapter_id = "cha1"
        chapter.series_id = "ser1"
        try:
            database.Session().add(chapter)
            database.Session.commit()
        except Exception:
            database.Session().rollback()
        print("sdasds")
        self.assertTrue(chapter_exists("ser1","cha1",database.Session()))