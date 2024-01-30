from sqlalchemy import or_, and_

from FMD3.core.database import DLDChapters, Session


def chapter_exists(series_id, chapter_id, session=Session, ):
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
    return bool(session.query(DLDChapters).filter(
        and_(
            DLDChapters.chapter_id == chapter_id, DLDChapters.series_id == series_id,
            # or_(
            #     DLDChapters.status == 0,
                # Only allow if added more than 30 minutes ago. Changed for active list in task manager
                # and_(
                #     DLDChapters.status == 2,
                #     DLDChapters.downloaded_at + timedelta(minutes=30) < datetime.now()
                # )
            )
    ).all())


def is_chapter_downloaded(series_id, chapter_id, session=Session):
    ...


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
