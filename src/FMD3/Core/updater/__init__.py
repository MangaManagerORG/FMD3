from FMD3.Core import database as db
from FMD3.Core.downloader import download_missing_chapters_from_series
from FMD3.Sources import get_sources_list


def new_chapters_finder():
    for source in get_sources_list():
        # get all series in favourites that are from this extension
        s = db.Session()

        series_list: list[db.Series] = s.query(db.Series).filter_by(source_id=source.ID).all()
        for series in series_list:
            last_db_chapter = series.max_chapter_number
            if last_db_chapter is not None:
                last_src_chapter = source.get_last_chapter(series.series_id)
                # Check if the last chapter form source is bigger. If not continue
                if last_src_chapter <= last_db_chapter:
                    print("Series has no new chapter")
                    continue
            data = source.on_get_info(series.series_id)
            # Proceed
            download_missing_chapters_from_series(source, series, data)
            print("DONWLOADING NEW CHAPTERS")
