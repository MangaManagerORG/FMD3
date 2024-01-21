from FMD3.Core.database import DLDChapters, Series, Session

def chapter_exists(series_id, chapter_id, session=Session,):
    """
        Check if a chapter with the specified `series_id` and `chapter_id` exists in the database.

        Parameters:
            series_id (str): The ID of the series to which the chapter belongs.
            chapter_id (str): The ID of the chapter to check for existence.

        Returns:
            bool: `True` if the chapter exists, `False` otherwise.
        """

    # return False
    session.flush()
    return bool(session.query(DLDChapters).filter_by(chapter_id=chapter_id, series_id=series_id).all())

def max_chapter_number(series_id):
    # Retrieve the max number from the DLDChapters table


    max_number = Session().query(DLDChapters.number).filter(
        DLDChapters.series_id == series_id).order_by(
        DLDChapters.number.desc()).first()

    # Return the max number if it exists, otherwise return None
    if max_number:
        return max_number.number
    else:
        return None
