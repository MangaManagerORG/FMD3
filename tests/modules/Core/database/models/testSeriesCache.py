import unittest
import datetime

from FMD3.core.database import SeriesCache
from FMD3.models.series_info import SeriesInfo

s = SeriesCache()
s.series_id = "testSeries_id"
s.cached_date = datetime.datetime.now()

s.title = "testSeries_title"
s.description = "testSeries_description"
s.authors = "testSeries_author"
s.artists = "testSeries_artist"
s.cover_url = "testSeries_cover_url"
s.genres = "testSeries_genres"
s.demographic = "testSeries_demographic"
s.rating = "testSeries_rating"
s.status = "testSeries_status"
s.url = "testSeries_url"

class TestSeriesCache(unittest.TestCase):
    def test_series_info(self):
        s_info = s.series_info
        self.assertEqual(s_info.id, "testSeries_id")
        self.assertEqual(s_info.genres, ["testSeries_genres"])


    def test_update(self):

        mi = SeriesInfo()
        mi.id = "testSeries_id"
        mi.title = "testSeries_title"
        mi.genres = ["testSeries_genres", "testSeries_genres_2"]

        s.update(mi)

        self.assertEqual(s.genres, "testSeries_genres,testSeries_genres_2")

