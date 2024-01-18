import csv
import re
import time
from pathlib import Path

import requests

from FMD3.Core.settings.models.SettingSection import SettingSection
from FMD3.Extensions import IExtension, add_extension
from FMD3.Models.Chapter import Chapter
from FMD3.Models.MangaInfo import MangaInfo

from .utils import get_demographic, get_rating, check_empty_chapters, check_group_id
from .Settings import Keys, controls

MANGAINFO = {}
_API_URL = 'https://api.mangadex.org'  # -- This is the url to the JSON API. Call this url to look at the API documentation.
_API_PARAMS = '?includes[]=author&includes[]=artist&includes[]=cover_art'
_COVER_URL = 'https://uploads.mangadex.org/covers'
_GUID_PATTERN = re.compile(r'.{8}-.{4}-.{4}-.{4}-.{12}')
# _MAPPING_FILE = 'userdata/mangadex_v5_mapping.txt'
_MAPPING_FILE = 'mangadex_v5_mapping.txt'

"""Dictionary with keypair values that maps v3 ids to v5"""
api_mapping = {}


class MangaDex(IExtension):
    ID = 'd07c9c2425764da8ba056505f57cf40c'
    Name = 'MangaDex'
    RootURL = 'https://mangadex.org'
    Category = 'English'
    # OnGetInfo = 'GetInfo'
    MaxTaskLimit = 1

    def init_settings(self):
        self.settings = [SettingSection(self.__class__.__name__, self.__class__.__name__, controls)]
        if Path(_MAPPING_FILE).exists():
            with open(_MAPPING_FILE, 'r') as mapping_file:
                for line in mapping_file:
                    old, new = line.split(";")
                    api_mapping[old] = new

    def on_get_pages_list(self, chapter_id) -> list[str]:
        # Extract chapter ID which is needed for getting info about the current chapter:
        # cid = split('chapter/')[1]
        # Delay this task if configured:
        # Delay()
        # Fetch JSON from API:
        pages = []
        r = requests.get(f'{_API_URL}/at-home/server/{chapter_id}?'.strip())
        if r.status_code != 200:
            return []

        data = r.json()
        url = data["baseUrl"].strip("/")
        hash = data["chapter"]["hash"]
        mode = "dataSaver" if self.get_setting(Keys.DATA_SAVER) else "data"
        links = []
        for image in data["chapter"]["data"]:
            links.append(f"{url}/{mode}/{hash}/{image}")
        # TODO: handle errors
        return links

    def on_get_name_and_link    (self):
        manga_names_link = []
        demographics = {
            1: 'shounen',
            2: 'shoujo',
            3: 'josei',
            4: 'seinen',
            5: 'none'
        }
        mangastatus = {
            1: 'ongoing',
            2: 'completed',
            3: 'hiatus',
            4: 'cancelled'
        }
        contentrating = {
            1: 'safe',
            2: 'suggestive',
            3: 'erotica',
            4: 'pornographic'
        }
        # Delay this task if configured:
        for _, dg in demographics.items():
            for _, ms in mangastatus.items():
                for _, cr in contentrating.items():
                    total = 1
                    offset = 0
                    offmaxlimit = 0
                    order = 'asc'
                    while total > offset:
                        time.sleep(5)
                        if total > 10000 and offset >= 10000 and order == 'asc':
                            offset = 0
                            order = 'desc'
                        if offset < 10000:
                            response = requests.get(_API_URL + '/manga?limit=200&offset=' + str(
                                offset) + '&order[createdAt]=' + order + '&publicationDemographic[]=' + dg + '&status[]=' + ms + '&contentRating[]=' + cr)
                            if response.status_code == 200:
                                # UPDATELIST.UpdateStatusText('Loading page of ' + dg + '/' + ms + '/' + cr + ' (' + order + ')' or '')
                                # x = CreateTXQuery(crypto.HTMLEncode(response.text))

                                data = response.json()
                                total = data["total"]
                                offset = offset + data["limit"]
                                manga_names_link.extend(
                                    [(item["attributes"]["title"]["en"], item["id"]) for item in data["data"]])
                        elif offset >= 10000:
                            offmaxlimit = total - 10000
                            print('Total Over Max Limit: ' + str(offmaxlimit) + ' are over the max limit!')

                        # todo: handle errors

        return manga_names_link

    def on_get_info(self, url) -> MangaInfo:
        # # Extract Manga ID which is needed for getting info and chapter list:
        # mid = URL.split('title/')[1] if 'title/' in URL else URL.split('manga/')[1]
        manga_id = None
        # Extract manga ID from URL
        mid = re.search(_GUID_PATTERN, url)

        # If no GUID (v5) was found, check if old ID (v3) is present
        if mid is None:
            # Old id
            # Extract manga ID from URL (v3)
            mid = re.search(r'\d{4}/(\d+)', url).group(1)
            # Check if GUID is mapped locally
            if mid:
                # Look up GUID for the extracted manga ID
                if mid in api_mapping:
                    manga_id = api_mapping[mid]
                    print('MangaDex: Legacy ID Mapping found in local text file:', mid)
                else:
                    # Retrieve GUID from legacy API endpoint
                    resp = requests.post(_API_URL + '/legacy/mapping', json={'type': 'manga', 'ids': [mid]})
                    if resp.status_code == 200 and resp.json()['success']:
                        newid = resp.json()['data'][0]['id']
                        print('MangaDex: Legacy ID Mapping retrieved from API:', newid)
                        manga_id = newid
        else:
            manga_id = mid.group()

        r = requests.get(_API_URL + "/manga/" + manga_id + _API_PARAMS)
        if r.status_code != 200:
            return
        print("asdsa")
        data = r.json()["data"]
        manga_data = self.get_info_parse_attributes(data, manga_id)
        chapters = self.get_info_parse_chapters(manga_id)
        manga_data.chapters = chapters
        return manga_data
        print("asdsa")
        # self._get_info_parse_attributes(data,manga_id)1
        # todo:handle errors

    def get_info_parse_chapters(self, manga_id) -> list[Chapter]:
        limitparam = 50
        langparam = f"translatedLanguage[]={self.get_setting(Keys.SelectedLanguage)}" if self.get_setting(
            Keys.SelectedLanguage) else []
        offset = 0
        # Handle chapters
        q = "&contentRating[]=safe&contentRating[]=suggestive&contentRating[]=erotica&contentRating[]=pornographic&includes[]=scanlation_group&order[volume]=asc&order[chapter]=asc"
        chapters = []
        total = 0
        iterations = 0
        while True:
            r = requests.get(
                _API_URL + "/manga/" + manga_id + f"/feed?limit={limitparam}&offset={offset}&{langparam}{q}")
            iterations += 1
            offset = limitparam * iterations

            if r.status_code != 200:
                return
            data = r.json()
            total = data["total"]

            chapters.extend([
                Chapter(id=chapter["id"],
                        volume=chapter["attributes"]["volume"],
                        number=float(chapter["attributes"]["chapter"]),
                        title=chapter["attributes"]["title"],
                        pages=chapter["attributes"]["pages"],
                        scanlator=None
                        # scanlator=list(filter(lambda x: x["type"] == "scanlation_group", chapter["relationships"]))[0][
                        #     "attributes"]["name"]
                        ) for chapter in data["data"]
                if check_empty_chapters(chapter["attributes"]) and check_group_id(
                    filter(lambda x: x["type"] == "scanlation_group", chapter["relationships"]))
            ])

            if total < 50:
                break
            elif iterations * limitparam >= total:
                break
        return chapters

    def get_info_parse_attributes(self, data, manga_id) -> MangaInfo:
        attributes = data["attributes"]
        mi = MangaInfo()
        mi.id = manga_id
        mi.title = attributes["title"]["en"]
        mi.alt_titles = attributes["altTitles"]
        mi.description = attributes["description"]["en"]
        mi.authors = list(author_data["attributes"]["name"] for author_data in filter(lambda x: x["type"] == "author", data["relationships"]))
        mi.artists = list(artist_data["attributes"]["name"] for artist_data in filter(lambda x: x["type"] == "artists", data["relationships"]))
        # MangaInfo.cover_art = list(filter(lambda x: x["type"] == "cover_art", data["relationships"]))
        covers = list(filter(lambda x: x["type"] == "cover_art", data["relationships"]))
        if covers:
            mi.cover_url = _COVER_URL + "/" + manga_id + "/" + covers[0]["attributes"]["fileName"]

        mi.genres = [tag["attributes"]["name"]["en"] for tag in
                     attributes["tags"] if tag["attributes"]["name"]["en"] is not None]  # Improvement: option to get locale tags?

        if get_demographic(demographic := attributes["publicationDemographic"]):
            mi.genres.append(demographic)
        mi.demographic = demographic

        if get_rating(rating := attributes["publicationDemographic"]):
            mi.rating = rating
            mi.genres.append(rating)

        if attributes["status"] in ("ongoing", "hiatus"):
            mi.status = "ongoing"
        else:
            mi.status = "completed"
        return mi


if __name__ == '__main__':
    MangaDex()

def load_extension():
    add_extension(MangaDex())
