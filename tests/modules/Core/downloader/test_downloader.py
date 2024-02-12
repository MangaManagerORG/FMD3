import io
import unittest
from tempfile import TemporaryFile
from zipfile import ZipFile

import requests

from FMD3.core.downloader.downloader import download_image, download_images_for_chapter
from FMD3.models.download_task import DownloadTask
img_url = "https://picsum.photos/200.jpg"


class TestDownloader(unittest.TestCase):

    def test_download_image(self):

        with requests.Session() as session:
            _img_url,data = download_image(session, img_url)
            self.assertIsInstance(data, io.BytesIO)

    def test_download_for_chapter(self):
        class Source:
            session = requests.Session()
        tsk = DownloadTask(Source,None,None,None,None)
        tsk._images_url = [img_url]

        download_images_for_chapter(tsk)

        for img in tsk.img_bytes_list:
            self.assertEqual(img[0],img_url)
            self.assertIsInstance(img[1], io.BytesIO)