from sqlalchemy import or_

from FMD3.core import database as db
from FMD3.core.TaskManager import TaskManager
from FMD3.models.ddl_chapter_status import DLDChaptersStatus as DDLCS

def get_hanging_tasks() -> list[db.DLDChapters]:
     return db.Session.query(db.DLDChapters).filter(or_(
             db.DLDChapters.status == DDLCS.ADDED_TO_QUEUE_SCANNER.value,
             db.DLDChapters.status == DDLCS.ADDED_TO_QUEUE_USER.value,
         )).all()


def get_active_tasks():
    tasks = [
        (f"{chapter.series_id}/{chapter.chapter_id}",chapter)
        for chapter in db.Session.query(db.DLDChapters).filter(or_(
            db.DLDChapters.status == DDLCS.ADDED_TO_QUEUE_SCANNER.value,
            db.DLDChapters.status == DDLCS.ADDED_TO_QUEUE_USER.value,
        )).all()
    ]

    active_mngr_tasks = TaskManager().active_tasks
    active_statuses = TaskManager().tasks_statuses
    active_tasks = [
        task for task in tasks if task[0] in active_mngr_tasks
    ]
    return [(t[1], active_statuses[t[0]]) for t in active_tasks]
