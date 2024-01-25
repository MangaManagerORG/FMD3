"""
Contains interfaces that the core will use to fetch info from the source
"""

from abc import abstractmethod

from FMD3.Models.Chapter import Chapter
from FMD3.Models.SeriesInfo import SeriesInfo


class ISourceMethods:
    def get_max_chapter(self, series_id: str) -> float:
        """
        Convenience method. uses get_chapters and sorts them
        Args:
            series_id:

        Returns:
        """

        chapters = self.get_chapters(series_id)
        last_chapter = list(filter(lambda x: x.number == max(chapter.number for chapter in chapters),
                                   chapters))
        if last_chapter:
            return last_chapter[0].number

    def get_new_chapters(self, series_id: str, last_chapter_in_db: float) -> list[Chapter]:
        """
        Convenience method. Uses get_chapters and sorts them.
        Gets all the chapters continuing last downloaded
        Args:
            series_id:
            last_chapter_in_db: Last chapter saved as downloaded in the database

        Returns: List of Chapters that have not been downloaded.
        """
        chapters = self.get_chapters(series_id)
        return list(filter(lambda x: x.number > last_chapter_in_db, chapters))

    @abstractmethod
    def get_chapters(self, series_id: str) -> list[Chapter]:
        """
        Gets all the chapters from a series
        Args:
            series_id:

        Returns:

        """

    def get_queried_chapters(self, series_id, chapters_ids: list[str]):
        return list(filter(lambda x: x.id in chapters_ids, self.get_chapters(series_id)))

    # @staticmethod
    # @abstractmethod
    # async def get_all_series() -> list[tuple[str, str]]:
    #     """
    #     Returns all the series available in the source.
    #     Args:
    #
    #     Returns:
    #
    #     """

    @abstractmethod
    def get_info(self, url) -> SeriesInfo:
        """
        Method that retrieves only basic series data.
        Args:
            url:

        Returns:

        """
        ...

    @abstractmethod
    def get_page_urls_for_chapter(self, chapter_id) -> list[str]:
        """
        Called when the core requests the list of pages (images url)
        :param chapter_id:
        :return:
        """
        ...

    @abstractmethod
    def find_series(self, query: str):
        ...

    @abstractmethod
    def init_settings(self):
        """
        Method called in extension initialization to load custom settings into main app
        -- Grabs extension settings and loads it to the base setting controller
        :return:
        """