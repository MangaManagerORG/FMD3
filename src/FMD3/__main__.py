import logging

from FMD3.core import database as db
from FMD3.core.database import Session
from FMD3.core.settings import Settings
from FMD3.core.settings import Keys
from FMD3.sources import get_extension, load_sources, get_source

# load_sources()

Settings()
Settings().set(Keys.CHAPTER_NAME,"Series - ${CHAPTER}")



ext = get_extension("MangaDex")


serie_url = "https://mangadex.org/title/41aea7f6-5ede-45d9-b7e6-7729acad4ea2/furyou-idol-chan"


def insert_default_series(serie_url):
    # user adds serie to favs
    data = ext.get_info(serie_url)

    # MM processes the data and adds series to favs
    try:
        series = db.Series(series_id=data.id, title=data.title)
        series.source_id = get_source("MangaDex").ID
        Session.add(series)
        Session.flush()
        Session.commit()
    except:
        # logging.getLogger().error("Error creating series")
        Session.rollback()
    return data

# insert_default_series(serie_url)
insert_default_series("https://mangadex.org/title/3d269f6e-10e1-4e4c-b453-48b38814494a/soukyuu-boys")
# insert_default_series("https://sandbox.mangadex.dev/title/d8323b7b-9a7a-462b-90f0-2759fed52511/hokkaido-gals-are-super-adorable")



series = Session.query(db.Series).filter_by(series_id="3d269f6e-10e1-4e4c-b453-48b38814494a").one()

# download_missing_chapters(ext, series, ext.get_chapters(series.series_id))
#
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
print("entering loop")
while 1:
    ...