from FMD3.core.database import DLDChapters
from FMD3.models.chapter import Chapter
from FMD3.models.series_info import SeriesInfo
from FMD3.extensions.sources import ISource

test_data = {
    "series_a": {
        "name": "Series A",
        "chapters": [
            {
                "id": "sAcha_1",
                "npages": 5,
                "number": 1,
                "volume": None,
                "pages": [
                    {
                        "id": "page_1",
                        "url": "url"
                    },
                    {
                        "id": "page_2",
                        "url": "url"
                    },
                    {
                        "id": "page_3",
                        "url": "url"
                    },
                    {
                        "id": "page_4",
                        "url": "url"
                    },
                    {
                        "id": "page_5",
                        "url": "url"
                    }
                ]
            },
            {
                "id": "sAcha_2",
                "npages": 10,
                "number": 2,
                "volume": None,
                "pages": [
                    {
                        "id": "page_1",
                        "url": "url"
                    },
                    {
                        "id": "page_2",
                        "url": "url"
                    },
                    {
                        "id": "page_3",
                        "url": "url"
                    },
                    {
                        "id": "page_4",
                        "url": "url"
                    },
                    {
                        "id": "page_5",
                        "url": "url"
                    }
                ]
            }
        ]
    },
    "series_b": {
        "name": "Series B",
        "chapters": [
            {
                "id": "sBcha_1",
                "npages": 5,
                "number": 1,
                "volume": None,
                "pages": [
                    {
                        "id": "page_1",
                        "url": "url"
                    },
                    {
                        "id": "page_2",
                        "url": "url"
                    },
                    {
                        "id": "page_3",
                        "url": "url"
                    },
                    {
                        "id": "page_4",
                        "url": "url"
                    },
                    {
                        "id": "page_5",
                        "url": "url"
                    }
                ]
            },
        ]
    }
}


class TestSource(ISource):
    @staticmethod
    def get_info(url) -> SeriesInfo:
        mi = SeriesInfo()
        mi.title = test_data.get(url).get("name")
        mi.id = url
        return mi

    def init_settings(self):
        pass

    def get_page_urls_for_chapter(self, chapter_id) -> list[str]:
        found_chapter = {}
        for series in test_data:
            if found_chapter:
                break
            for chapter in test_data[series]["chapters"]:
                if found_chapter:
                    break
                if chapter["id"] == chapter_id:
                    found_chapter = chapter
                    break

        return [page["url"] for page in found_chapter["pages"]]

    @staticmethod
    def get_all_series() -> list[tuple[str, str]]:
        return [(test_data[series]["name"], series) for series in test_data]

    def get_chapters(self, series_id: str) -> list[Chapter]:
        for series in test_data:
            if series == series_id:
                return [Chapter(
                    chapter_id=chapter["id"],
                    title="",
                    number=chapter["number"],
                    volume=chapter["volume"],
                    pages=chapter["npages"],
                    scanlator=None
                )
                    for chapter in test_data[series]["chapters"]]

    def _debug_get_chapter(self, series_id, chapter_id) -> Chapter | None:

        filtered_chapter = list(filter(lambda x: x.chapter_id == chapter_id, self.get_chapters(series_id=series_id)))
        if filtered_chapter:
            return filtered_chapter[0]
        return None

    def get_queried_chapters(self, series_id, chapters_ids: list[DLDChapters]):
        return list(filter(lambda x: x.chapter_id in chapters_ids, self.get_chapters(series_id)))

    ID = "TESTSOURCE"
    NAME = "TESTSOURCE"
    ROOT_URL = ""
    CATEGORY = ""
