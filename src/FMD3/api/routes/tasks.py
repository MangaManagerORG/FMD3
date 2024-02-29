from sqlalchemy import or_, and_

from FMD3.core import database as db
from FMD3.core.TaskManager import TaskManager
from FMD3.models.ddl_chapter_status import DLDChaptersStatus as DDLCS
from FMD3.api.models.tasks import HangingTaskResponse


def get_hanging_tasks() -> list[db.DLDChapters]:
    return db.Session.query(db.DLDChapters).filter(or_(
        db.DLDChapters.status == DDLCS.ADDED_TO_QUEUE_SCANNER,
        db.DLDChapters.status == DDLCS.ADDED_TO_QUEUE_USER,
    )).all()


def get_active_tasks():
    tasks = [
        (f"{chapter.series_id}/{chapter.chapter_id}", chapter)
        for chapter in db.Session.query(db.DLDChapters).filter(or_(
            db.DLDChapters.status == DDLCS.ADDED_TO_QUEUE_SCANNER,
            db.DLDChapters.status == DDLCS.ADDED_TO_QUEUE_USER,
        )).all()
    ]

    active_mngr_tasks = TaskManager().active_tasks
    active_statuses = TaskManager().tasks_statuses
    active_tasks = [
        task for task in tasks if task[0] in active_mngr_tasks
    ]
    return [(t[1], active_statuses[t[0]]) for t in active_tasks]


def get_recent_tasks() -> list[HangingTaskResponse]:
    tasks = db.Session.query(
            db.Series.title,
            db.DLDChapters.status,
            db.Series.source_id,
            db.DLDChapters.path,
            db.DLDChapters.added_at,
            db.DLDChapters.downloaded_at,
            db.DLDChapters.volume,
            db.DLDChapters.number,
            db.DLDChapters.chapter_id,
            db.Series.series_id
        ).join(db.Series).filter(and_(
            db.DLDChapters.status != DDLCS.ADDED_TO_QUEUE_SCANNER,
            db.DLDChapters.status != DDLCS.ADDED_TO_QUEUE_USER,
        )).order_by(db.DLDChapters.downloaded_at).limit(200).all()
    data = [
        HangingTaskResponse(**row._mapping)
        for row in tasks
    ]
    return data