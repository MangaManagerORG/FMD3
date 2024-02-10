import unittest
from unittest.mock import patch, MagicMock

from FMD3.core.downloader.utils import analyze_archive
from FMD3.models.chapter import Chapter
from tests.mockzip import MockZip


class TestAnalyzeArchive(unittest.TestCase):
    ...
    @patch("FMD3.core.downloader.utils.Path.exists",return_value=True)
    @patch("FMD3.core.downloader.utils.ZipFile",new_callable=MockZip)
    def test_analyze_should_skip_files(self,mock_zip:MagicMock,*_):
        def namelist(*_):
            return ["ComicInfo.xml", "img1.jpg", "img2.jpg"]
        MockZip.namelist = namelist
        # mock_zip.files = ["ComicInfo.xml","img1.jpg","img2.jpg"]
        c = Chapter("id",None,None,None,2,None)
        self.assertTrue(analyze_archive("output_file", "serie_id",c))

    @patch("FMD3.core.downloader.utils.Path.exists",return_value=True)
    @patch("FMD3.core.downloader.utils.ZipFile",new_callable=MockZip)
    def test_analyze_should_detect_broken(self,mock_zip:MagicMock,*_):
        def namelist(*_):
            return ["ComicInfo.xml", "img2.jpg"]
        MockZip.namelist = namelist
        # mock_zip.files = ["ComicInfo.xml","img1.jpg","img2.jpg"]
        c = Chapter("id",None,None,None,2,None)
        self.assertFalse(analyze_archive("output_file", "serie_id",c))
