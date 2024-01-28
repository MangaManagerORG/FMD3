import unittest
from pathlib import Path

from FMD3.Core.settings import Settings
from FMD3.Core.settings import Keys
from FMD3.Core.utils import get_series_folder_name, get_chapter_name
from FMD3.errors import TemplateMissingTag


class TestTemplatesFolderName(unittest.TestCase):
    def test_series_folder_name_template(self):
        """
        Tests that the folder name for a given series is created successfully from the user preferences input
        Returns:
        """
        Settings().set(Keys.DEFAULT_DOWNLOAD_PATH, ".")
        Settings().set(Keys.SERIES_FOLDER_NAME, "${MANGA}")

        folder_name = get_series_folder_name(website="website", manga="manga", author="author", artist="artist")

        self.assertEqual(Path(folder_name), Path("./manga"))

    def test_folder_template_no_manga_tag_should_raise_exception(self):
        """
        Tests that an exception is raised when the user has no ${MANGA}  in preference string template
        Returns:

        """
        Settings().set(Keys.DEFAULT_DOWNLOAD_PATH, ".")
        Settings().set(Keys.SERIES_FOLDER_NAME, "${WEBSITE}")
        self.assertRaises(TemplateMissingTag, get_series_folder_name, website="website", manga="manga", author="author",
                          artist="artist")

        # self.assertEqual(Path(folder_name), Path("./manga"))

    def test_folder_template_no_attr_should_raise_exception(self):
        """
        Test that exception is raised if no Manga attr is provided
        Returns:

        """
        Settings().set(Keys.DEFAULT_DOWNLOAD_PATH, ".")
        Settings().set(Keys.SERIES_FOLDER_NAME, "${WEBSITE}")
        self.assertRaises(KeyError, get_series_folder_name, website="website", author="author", artist="artist")


class TestTemplatesChapterName(unittest.TestCase):
    def test_chapter_name_template(self):
        """
        Tests that the chapter name for a given chapter is created successfully from the user preferences input
        Returns:
        """
        Settings().set(Keys.CHAPTER_NAME, "${MANGA} ${WEBSITE} [${AUTHOR}] - ${VOLUME} ${CHAPTER}")

        attr = {"website": "_website_",
                "manga": "_manga_",
                "chapter": 6,
                "author": "_author_",
                "artist": "_artist_",
                "volume": 7}
        chapter_name = get_chapter_name(**attr)
        # self.assertEqual(Path(folder_name), Path("./manga"))
        self.assertEqual("_manga_ _website_ [_author_] - Vol.07 Ch.006", chapter_name)

    # Settings().set(SaveTo, SaveTo.CHAPTER_NAME, "${MANGA} - ${VOLUME} ${Chapter} ")
    def test_chapter_name_template_should_clean_brackets_if_key_not_present(self):
        """
        Test that if a key between brackets is not present, brackets are cleaned up
        Returns:
        """
        Settings().set(Keys.CHAPTER_NAME, "${MANGA} ${WEBSITE} [${AUTHOR}] - ${VOLUME} ${CHAPTER}")

        attr = {"website": "_website_",
                "manga": "_manga_",
                "chapter": 6,
                "author": None,
                "artist": "_artist_",
                "volume": 7}
        chapter_name = get_chapter_name(**attr)
        # self.assertEqual(Path(folder_name), Path("./manga"))
        self.assertEqual("_manga_ _website_ - Vol.07 Ch.006",chapter_name)

    # Settings().set(SaveTo, SaveTo.CHAPTER_NAME, "${MANGA} - ${VOLUME} ${Chapter} ")

    def test_chapter_template_no_chapter_tag_should_raise_exception(self):
        """
        Tests that an exception is raised when the user has no ${CHAPTER} or ${NUMBERING} in preference string template
        Returns:

        """

        Settings().set(Keys.CHAPTER_NAME, "${MANGA} - ${VOLUME}")
        attr = {"website": None,
                "manga": None,
                "chapter": 3,
                "author": None,
                "artist": None,
                "volume": None}

        self.assertRaises(TemplateMissingTag, get_chapter_name, **attr)

    def test_chapter_template_no_chapter_attr_should_raise_exception(self):
        """
        Test that exception is raised if no chapter attr is provided
        Returns:

        """
        # Settings().set(SaveTo, SaveTo.DEFAULT_DOWNLOAD_PATH, ".")
        # Settings().set(SaveTo, SaveTo.SERIES_FOLDER_NAME, "${WEBSITE}")
        Settings().set(Keys.CHAPTER_NAME, "${MANGA} - ${VOLUME} ${CHAPTER}")
        attr = {"website": None,
                "manga": None,
                # "chapter":None,
                "author": None,
                "artist": None,
                "volume": None}
        self.assertRaises(KeyError, get_chapter_name, **attr)

    def test_chapter_template_volume_is_none_should_not_leave_space(self):
        """
        Test that checks that if a volume is None, there will be no extra spaces (since tag will be ommited is missing)
        Returns:

        """
        Settings().set(Keys.CHAPTER_NAME, "${MANGA} - ${VOLUME} ${CHAPTER}")
        attr = {"website": None,
                "manga": "_manga_name_",
                "chapter": 3,
                "author": None,
                "artist": None,
                "volume": None}
        ch_name = get_chapter_name(**attr)
        self.assertEqual("_manga_name_ - Ch.003", ch_name)
