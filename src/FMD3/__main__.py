from string import Template

from FMD3.Core.settings import Settings
from FMD3.Core import load_sources
from FMD3.Core import database as db
from FMD3.Core.database.Session import Session
from FMD3.Core.settings.Keys import SaveTo
from FMD3.Sources import get_extension

#
# for extension in extesion_factory:
#     extension.print_ext_name()fr
from FMD3.Core.logging import setup_logging, TRACE

setup_logging("config/log.log",TRACE)
load_sources()
ext = get_extension("MangaDex")




# Check if Flask is installed
# if 'Flask' in sys.modules:
# Run the web UI if Flask is installed

# local = db.get_session()

serie_url = "https://mangadex.org/title/41aea7f6-5ede-45d9-b7e6-7729acad4ea2/furyou-idol-chan"
def test_download(serie_url):
    # user adds serie to favs
    data = ext.on_get_info(serie_url)


    # MM processes the data and adds series to favs
    try:
        series = db.Series(series_id=data.id,title=data.title)
        db.session.add(series)
        db.session.flush()
        db.session.commit()
    except:
        db.session.rollback()


    ## Process checking for new chapters::
    series = Session.query(db.Series).filter_by(series_id=data.id).one()
    new_chapters = (ext, series, data.chapters)


    # download_missing_chapters_from_series(ext,series,data)


    series = Session.query(db.Series).all()

    for serie in series:
        print("====================")
        print("--------------------")
        # print(f"Series: {series.title}")
        for chapter in serie.chapters:
            print(f"Chapter: {chapter.number}")
            print(f"Title: {chapter.title}")



Settings().set(SaveTo,SaveTo.SERIES_FOLDER_NAME,"manga_name: $manga author: $author")
s = Settings().get(SaveTo, SaveTo.SERIES_FOLDER_NAME)

t= Template(s)
res = t.safe_substitute(
    website = "_web_",
    manga = "_manga_",
    author = "_author_"
)
print(res)
print("asdsa")
# #
# # download([
# #     (ext,[])
# # ]
# # # )
# #
# # # import FMD3.DumbUI



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