import io
from tempfile import TemporaryFile
from unittest import TestCase
from unittest.mock import patch, MagicMock

from ComicInfo import ComicInfo
from PIL import Image

from FMD3.core.downloader.processing import convert_image, convert_and_zip
from FMD3.models.ddl_chapter_status import DLDChaptersStatus
from FMD3.models.download_task import DownloadTask
from tests.TestSource.TestSource import TestSource

img = Image.new(mode="RGB", size=(200, 200))
image = io.BytesIO()
img.save(image, "PNG")
class TestProcessing(TestCase):
    def test_convert_image(self):
        convert_image(image)


class TestConvertAndZip(TestCase):
    @patch("FMD3.core.downloader.processing.convert_image",return_value=image)
    def test_convert_and_zip(self, *_):
        source = TestSource()
        series,saveto = source.get_series_info("series_a")
        chapter = source.get_chapters(series.id)[0]
        with TemporaryFile() as f:
            task = DownloadTask(
                source=source,
                series_id=series.id,
                chapter=chapter,
                output_path=f,
                cinfo=ComicInfo()
            )

            task.img_bytes_list = [("url.jpg",image)]

            a = convert_and_zip(task)
            self.assertEqual(DLDChaptersStatus.DOWNLOADED,a.status)

    @patch("FMD3.core.downloader.processing.convert_image", side_effect=Exception())
    def test_convert_and_zip_convert_fail_should_use_raw_image(self,exception:MagicMock):
        source = TestSource()
        series, saveto = source.get_series_info("series_a")
        chapter = source.get_chapters(series.id)[0]
        with TemporaryFile() as f:
            task = DownloadTask(
                source=source,
                series_id=series.id,
                chapter=chapter,
                output_path=f,
                cinfo=ComicInfo()
            )

            task.img_bytes_list = [("url.jpg", image)]

            a = convert_and_zip(task)
            exception.assert_called()
            self.assertEqual(DLDChaptersStatus.DOWNLOADED, a.status)

    @patch("FMD3.core.downloader.processing.is_convert", return_value=False)
    @patch("FMD3.core.downloader.processing.convert_image", side_effect=Exception())
    def test_convert_should_not_convert(self,exception:MagicMock, *_):
        source = TestSource()
        series, saveto = source.get_series_info("series_a")
        chapter = source.get_chapters(series.id)[0]
        with TemporaryFile() as f:
            task = DownloadTask(
                source=source,
                series_id=series.id,
                chapter=chapter,
                output_path=f,
                cinfo=ComicInfo()
            )

            task.img_bytes_list = [("url.jpg", image)]

            a = convert_and_zip(task)
            exception.assert_called()
            self.assertEqual(DLDChaptersStatus.DOWNLOADED, a.status)

    @patch("FMD3.core.downloader.processing.is_convert", return_value=False)
    @patch("FMD3.core.downloader.processing.ZipFile.writestr", side_effect=Exception())
    def test_convert_write_str_raises(self, exception: MagicMock, *_):
        source = TestSource()
        series, saveto = source.get_series_info("series_a")
        chapter = source.get_chapters(series.id)[0]
        with TemporaryFile() as f:
            task = DownloadTask(
                source=source,
                series_id=series.id,
                chapter=chapter,
                output_path=f,
                cinfo=ComicInfo()
            )

            task.img_bytes_list = [("url.jpg", image)]

            a = convert_and_zip(task)
            exception.assert_called()
            self.assertEqual(DLDChaptersStatus.ERRORED, a.status)

    @patch("FMD3.core.downloader.processing.is_convert", return_value=False)
    @patch("FMD3.core.downloader.processing.ZipFile.writestr", side_effect=Exception())
    def test_convert_write_str_raises_opening_zipfile(self, exception: MagicMock, *_):
        source = TestSource()
        series, saveto = source.get_series_info("series_a")
        chapter = source.get_chapters(series.id)[0]
        with TemporaryFile() as f:
            task = DownloadTask(
                source=source,
                series_id=series.id,
                chapter=chapter,
                output_path=f,
                cinfo=ComicInfo()
            )

            task.img_bytes_list = [("url.jpg", image)]

            a = convert_and_zip(task)
            exception.assert_called()
            self.assertEqual(DLDChaptersStatus.ERRORED, a.status)

