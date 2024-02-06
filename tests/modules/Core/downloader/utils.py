import unittest
from unittest.mock import MagicMock, patch

from ComicInfo import ComicInfo

from FMD3.core.downloader import append_cinfo
from . import MockZipf

class TestDownloaderUtils(unittest.TestCase):


    @patch("FMD3.core.downloader.utils.ZipFile",new_callable=MockZipf)
    def test_info_appended(self,mocked_Zipfile:MagicMock,*args):
        mock = MagicMock()
        MockZipf.writestr = mock


        cinfo = ComicInfo()
        append_cinfo("file.zip",cinfo)
        mock.assert_called_with("ComicInfo.xml", cinfo.to_xml())