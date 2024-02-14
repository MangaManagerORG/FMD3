import dataclasses
import io

import ComicInfo

from FMD3.models.chapter import Chapter
from FMD3.models.ddl_chapter_status import DLDChaptersStatus


@dataclasses.dataclass
class DownloadTask:
    source: object
    series_id: str
    chapter: Chapter
    output_path: str
    cinfo: ComicInfo
    _images_url: list[str]

    img_bytes_list: list[tuple[str, io.BytesIO]]
    status: DLDChaptersStatus = DLDChaptersStatus.NOT_DOWNLOADED

    def __init__(self, source, series_id: str, chapter: Chapter, output_path: str, cinfo: ComicInfo):
        self.source = source
        self.series_id = series_id
        self.chapter = chapter
        self.output_path = output_path
        self.cinfo = cinfo
        self._images_url = []
        self.img_bytes_list = []

    @property
    def images_url(self) -> list[str]:
        if not self._images_url:
            self._images_url = self.source.get_page_urls_for_chapter(self.chapter.chapter_id)
        return self._images_url
