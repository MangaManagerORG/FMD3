from FMD3.Core.database import DLDChapters, Series, Session
from FMD3.Models.Chapter import Chapter


def chapter_exists(series_id, chapter_id):
    """
        Check if a chapter with the specified `series_id` and `chapter_id` exists in the database.

        Parameters:
            series_id (str): The ID of the series to which the chapter belongs.
            chapter_id (str): The ID of the chapter to check for existence.

        Returns:
            bool: `True` if the chapter exists, `False` otherwise.
        """

    # return False
    return bool(Session.query(DLDChapters).filter_by(chapter_id=chapter_id, series_id=series_id).all())