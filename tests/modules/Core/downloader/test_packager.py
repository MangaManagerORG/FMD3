import unittest
from unittest.mock import patch, MagicMock
from ComicInfo import ComicInfo

from FMD3.core.database.models import DLDChaptersStatus
from FMD3.core.downloader import download_series_chapter
from FMD3.models.chapter import Chapter
from TestSource.TestSource import TestSource


class TestDownloadChapter(unittest.TestCase):

    @patch("FMD3.core.downloader.analyze_archive", return_value=False)
    @patch("FMD3.core.downloader.download_n_pack_pages",
           return_value=[("img1.jpg", b"img1_data"), ("img2.jpg", b"img2_data")])
    @patch("FMD3.core.downloader.append_cinfo", return_value=None)
    def test_download_chapter_success(self, mock_analyze, mock_download_pages, mock_append_cinfo):
        series_id = "123"
        chapter_id = "456"
        output_file_path = "output.zip"
        source = TestSource()
        source.get_page_urls_for_chapter = lambda x: ["img1_url", "img2_url"]
        ret = download_series_chapter(source, "series_a", Chapter("chapter_a1",None,None,None,None,None), "output", ComicInfo())
        self.assertEqual(ret[2], DLDChaptersStatus.DOWNLOADED)

    @patch("FMD3.core.downloader.analyze_archive", return_value=True)
    @patch("FMD3.core.downloader.download_n_pack_pages",
           return_value=[("img1.jpg", b"img1_data"), ("img2.jpg", b"img2_data")])
    @patch("FMD3.core.downloader.append_cinfo", return_value=None)
    def test_download_chapter_skipped(self, mock_analyze, mock_download_pages, mock_append_cinfo):
        source = TestSource()
        source.get_page_urls_for_chapter = lambda x: ["img1_url", "img2_url"]
        ret = download_series_chapter(source, "series_a", Chapter("chapter_a1", None, None, None, None, None), "output",
                                      ComicInfo())
        self.assertEqual(ret[2], DLDChaptersStatus.SKIPPED)

    # @patch("your_module.analyze_archive", return_value=True)
    # def test_download_chapter_skip(self, mock_analyze):
    #     series_id = "123"
    #     chapter_id = "456"
    #     output_file_path = "output.zip"
    #
    #     result = analyze_archive(output_file_path, series_id, chapter_id)
    #
    #     self.assertTrue(result)  # File should be skipped
    #
    #     series_id, chapter_id, status = asyncio.run(download_chapter(series_id, chapter_id, output_file_path))
    #
    #     self.assertEqual(status, DLDChaptersStatus.SKIPPED)
    #     mock_analyze.assert_called_once_with(output_file_path, series_id, chapter_id)
    #     # Add more assertions as needed

    # Add more test cases for error scenarios
