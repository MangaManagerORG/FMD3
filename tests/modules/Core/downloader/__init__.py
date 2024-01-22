import unittest
from tempfile import TemporaryFile
from unittest.mock import patch, Mock, MagicMock
from zipfile import ZipFile

from ComicInfo import ComicInfo
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from FMD3.Core.database import Base, Series, DLDChapters
from FMD3.Core.database.predefined import chapter_exists
from FMD3.Core.downloader import download_n_pack_pages, download_series_chapter, download_image
from TestSource import TestSource


def create_session():
    engine = create_engine('sqlite:///', isolation_level="SERIALIZABLE")
    session_factory = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    session = scoped_session(session_factory)
    session.rollback()
    return session
def scoped_session(*_):
    engine = create_engine('sqlite:///', isolation_level="SERIALIZABLE")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    return scoped_session(session_factory)
class MockZipf(MagicMock):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.files = []

    def __iter__(self):
        return iter(self.files)

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        return True
    def writestr(self,*args,**kwargs):
        ...

class TestDownload(unittest.TestCase):

    @patch("FMD3.Core.downloader.ZipFile")
    @patch("FMD3.Core.downloader.download_image")
    def test_downloading_pages(self, download_image_mock:MagicMock, zip_patch):

        zip_patch = MockZipf
        zip_patch.files = [Mock(filename="f1.cbz")]
        url_list = ["url1.jpeg","url2.jpeg","url3.jpeg"]
        download_n_pack_pages("f1.cbz",url_list)
        print("sadas")

        for i, pack in enumerate(zip(download_image_mock.call_args_list,url_list)):
            call,url = pack
            self.assertEqual(call.args[1],url)
            download_image_mock(url,str(i).zfill(3) + ".jpeg")

    @unittest.skip("Needs to be remade")
    @patch("FMD3.Core.downloader.scoped_session",new_callable=scoped_session)
    @patch("FMD3.Core.downloader.download_image")
    def test_download_series_chapter(self,dld,session,*args):
        # patch db session
        # Insert series
        s = Series()
        s.series_id = "series_a"
        s.source_id = TestSource.ID
        session.add(s)
        session.commit()
        # Confirm chapter did not exist prev
        check = lambda :bool(session.query(DLDChapters).filter_by(chapter_id="sAcha_1", series_id="series_a").all())
        self.assertFalse(check())
        cinfo = ComicInfo()
        self.assertTrue(download_series_chapter(TestSource(), "series_a",TestSource()._debug_get_chapter("series_a","sAcha_1"),"f1.cbz",cinfo))

        # Assert flow is compleed and chapter is added to db
        self.assertTrue(check())
    @unittest.skip("Invalid")
    def test_download_image(self):
        img_url = "https://picsum.photos/200.jpg"
        with TemporaryFile() as f:
            with ZipFile(f,"w") as zout:
                download_image(img_url, "image_a.jpg")
            self.assertIn("image_a.jpg",zout.namelist())
