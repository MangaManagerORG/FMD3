import logging
import threading
import time
from string import Template

import schedule

from FMD3.Core.database.predefined import chapter_exists
from FMD3.Core.downloader import download_missing_chapters_from_series
from FMD3.Core.scheduler import start_fav_scan_schedule, run_scheduler
from FMD3.Core.settings import Settings
from FMD3.Core import database as db
from FMD3.Core.database.Session import Session
from FMD3.Core.settings.Keys import SaveTo
from FMD3.Core.updater import new_chapters_finder
from FMD3.Enrichers import iterate_enrichers
from FMD3.Models.Chapter import Chapter
from FMD3.Sources import get_extension, load_sources, get_source

#
# for extension in extesion_factory:
#     extension.print_ext_name()fr
from FMD3.Core.logging import setup_logging, TRACE

setup_logging("config/log.log", TRACE)
load_sources()

ext = get_extension("MangaDex")
import FMD3.DumbUI
# Check if Flask is installed
# if 'Flask' in sys.modules:
# Run the web UI if Flask is installed

# local = db.get_session()

serie_url = "https://mangadex.org/title/41aea7f6-5ede-45d9-b7e6-7729acad4ea2/furyou-idol-chan"


def insert_default_series(serie_url):
    # user adds serie to favs
    data = ext.on_get_info(serie_url)

    # MM processes the data and adds series to favs
    try:
        series = db.Series(series_id=data.id, title=data.title)
        series.source_id = get_source("MangaDex").ID
        db.session.add(series)
        db.session.flush()
        db.session.commit()
    except:
        logging.getLogger().error("Error creating series")
        db.session.rollback()


insert_default_series(serie_url)
# new_chapters_finder()
print("sadsada")

start_fav_scan_schedule()
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()

# User wants to download TheNewGate
url = "https://mangadex.org/chapter/229db249-914b-4ee1-a71b-b03894c481af"

# Source fetches info about it:
series_info = ext.get_info(url)

# Source fetches chapters in it:
manga_chapters: list[Chapter] = ext.get_chapters(series_info.id)

# Filter downloaded chapters]
manga_chapters = list(filter(lambda chapter: chapter_exists(series_info.id, chapter.id),
                             manga_chapters))

final_series_info = []

for chapter in manga_chapters:
    final_series_info = iterate_enrichers(series_info, chapter)






































# from sqlalchemy import exc
# logger = logging.getLogger()
# def thread_function():
#     local_session = Session()
#     # chapterObj = db.DLDChapters(chapter_id="12345", series_id="67890", number=1)
#     # local_session.add(chapterObj)
#     # local_session.flush()
#     try:
#         # Insert a new record in the DLDChapters table
#         # Raise an integrity error to simulate a unique constraint violation
#         local_session.add(db.DLDChapters(chapter_id="12345", series_id="67890", number=1))
#         local_session.flush()
#         local_session.commit()
#     except exc.IntegrityError as e:
#         logger.exception("Integrity error in thread A")
#         local_session.rollback()
#     finally:
#         Session.remove()
#
# def thread_function2():
#     local_session = Session()
#     try:
#         # Insert a new record in the DLDChapters table
#         chapterObj = db.DLDChapters(chapter_id="54321", series_id="67890", number=1)
#         local_session.add(chapterObj)
#         local_session.flush()
#         local_session.commit()
#     except exc.IntegrityError as e:
#         logger.exception("Integrity error in thread A")
#         local_session.rollback()
#     finally:
#         Session.remove()
#
# thread = threading.Thread(target=thread_function)
# thread2 = threading.Thread(target=thread_function2)
# # chapterObj = db.DLDChapters(chapter_id="adadas", series_id="67890", number=1)
# # db.session.add(chapterObj)
# # db.session.flush()
# thread2.start()
# thread.start()
# thread.join()
# thread2.join()
# # db.session.commit()
# print(db.Session().query(db.DLDChapters).all())
# print("sada")
