import csv
import re
import time

import requests

from FMD3.Core.settings.models.SettingSection import SettingSection
from FMD3.Extensions import IExtension, add_Extension

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


class MangaInfo:
    ...


class MangaDex(IExtension):

    ...
    ext_setting_controls = []

    def init_settings(self):
        self.settings = [SettingSection(self.__class__.__name__, controls)]
        with open(_MAPPING_FILE, 'r') as mapping_file:
            for line in mapping_file:
                old, new = line.split(";")
                api_mapping[old] = new

    def __init__(self):
        print("init")
        ...

        self.ID = 'd07c9c2425764da8ba056505f57cf40c'
        self.Name = 'MangaDex'
        self.RootURL = 'https://mangadex.org'
        self.Category = 'English'
        self.OnGetInfo = 'GetInfo'

        self.OnGetPageNumber = 'GetPageNumber'

        self.OnGetNameAndLink = 'GetNameAndLink'

        self.OnGetDirectoryPageNumber = 'GetDirectoryPageNumber'
        self.OnLogin = 'Login'
        self.OnAccountState = 'AccountState'

        self.MaxTaskLimit = 1
        # self.MaxConnectionLimit = 2
        # self.AccountSupport = True

        # self.AddServerCookies('mangadex.org', 'mangadex_h_toggle=1; max-age=31556952')
        # fmd = require('fmd.env')
        slang = Keys.SelectedLanguage
        # lang = {
        #     'en': {
        #         'delay': 'Delay (s) between requests',
        #         'showscangroup': 'Show scanlation group',
        #         'showchaptertitle': 'Show chapter title',
        #         'lang': 'Language:'
        #     },
        #     'id_ID': {
        #         'delay': 'Tunda (detik) antara permintaan',
        #         'showscangroup': 'Tampilkan grup scanlation',
        #         'showchaptertitle': 'Tampilkan judul bab',
        #         'lang': 'Bahasa:'
        #     },
        #     'get': lambda self, key: self[slang][key] if slang in self and key in self[slang] else self['en'][key]
        # }
        # self.AddOptionSpinEdit('mdx_delay', lang['get']('delay'), 2)
        # self.AddOptionCheckBox('luashowscangroup', lang['get']('showscangroup'), False)
        # self.AddOptionCheckBox('luashowchaptertitle', lang['get']('showchaptertitle'), True)
        # items = 'All'
        # req_delay =

        # Legacy lua code:
        # t = GetLangList()
        # for v in t:
        #     items += '\r\n' + v
        # Adds an option
        # self.AddOptionComboBox('lualang', lang['get']('lang'), items, 11)
        self.on_get_page_number("fe555074-2ed0-4f8d-8706-e56930e38e1f")
        # self.on_get_info('https://mangadex.org/title/911f2f01-9718-4a42-8e2a-1b684b695cba/df')


    def on_get_page_number(self, chapter_id):
        # Extract chapter ID which is needed for getting info about the current chapter:
        # cid = split('chapter/')[1]
        # Delay this task if configured:
        # Delay()
        # Fetch JSON from API:
        pages = []
        r = requests.get(f'{_API_URL}/at-home/server/{chapter_id}?'.strip())
        if r.status_code != 200:
            return

        data = r.json()
        cinfo = data['base_url']
        url = data["baseUrl"].strip("/")
        hash = data["chapter"]["hash"]
        mode = ["dataSaver" if self.get_setting(Keys.DATA_SAVER) else "data"]
        links = []
        for image in data["chapter"]:
            links.append(f"{url}+/{mode}+{hash}+{image}")
        # TODO: handle errors
        return links

    def on_get_name_and_link(self):
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
    def on_get_info(self, URL):
        # # Extract Manga ID which is needed for getting info and chapter list:
        # mid = URL.split('title/')[1] if 'title/' in URL else URL.split('manga/')[1]
        manga_id = None
        # Extract manga ID from URL
        mid = re.search(_GUID_PATTERN, URL)

        # If no GUID (v5) was found, check if old ID (v3) is present
        if mid is None:
            # Old id
            # Extract manga ID from URL (v3)
            mid = re.search(r'\d{4}/(\d+)', URL).group(1)
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
        manga_data = self.parse_attributes(data, manga_id)
        chapters = self.parse_chapters(manga_id)
        # todo:handle errors

    def _get_info_parse_chapters(self, manga_id):
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
                chapter for chapter in data
                if check_empty_chapters(chapter["attributes"]) and check_group_id(
                    filter(lambda x: x["type"] == "scanlation_group", chapter["relationships"]))
            ])

            if total < 50:
                break
            elif iterations * limitparam >= total:
                break
        return chapters
    def _get_info_parse_attributes(self, data, manga_id):
        atributes = data["attributes"]
        MangaInfo.Title = atributes["title"]
        MangaInfo.altTitles = atributes["altTitles"]
        MangaInfo.description = atributes["description"]
        MangaInfo.authors = list(filter(lambda x: x["type"] == "author", data["relationships"]))
        MangaInfo.artists = list(filter(lambda x: x["type"] == "artists", data["relationships"]))
        # MangaInfo.cover_art = list(filter(lambda x: x["type"] == "cover_art", data["relationships"]))
        covers = list(filter(lambda x: x["type"] == "cover_art", data["relationships"]))
        if covers:
            MangaInfo.cover_url = _COVER_URL + "/" + manga_id + covers[0]["attributes"]["fileName"]

        MangaInfo.genres = [tag["attributes"]["name"]["en"] for tag in
                            atributes["tags"]]  # Improvement: option to get locale tags?

        if get_demographic(demographic := atributes["publicationDemographic"]):
            MangaInfo.genres.append(demographic)
        MangaInfo.demographic = demographic

        if get_rating(rating := atributes["publicationDemographic"]):
            MangaInfo.rating = rating
            MangaInfo.genres.append(rating)

        if atributes["status"] in ("ongoing", "hiatus"):
            MangaInfo.status = "ongoing"
        else:
            MangaInfo.status = "completed"
        return MangaInfo




if __name__ == '__main__':
    MangaDex()
#     on_get_info(None, "https://mangadex.org/title/fac533c1-baeb-4dc5-af60-8792abe463a3")

# json = {'result': 'ok', 'response': 'entity',
#         'data': {
#             'id': 'fac533c1-baeb-4dc5-af60-8792abe463a3',
#             'type': 'manga',
#             'attributes': {
#                 'title': {'en': 'Bloodline'},
#                 'altTitles': [
#                     {'zh': '血族BLOODLINE'},
#                     {'zh-hk': '血族BLOODLINE：聖魔虛像篇'},
#                     {'en': 'Bloodline: Illusion of the Holy Demon'},
#                     {'zh': '血族Bloodline：圣魔虚像篇'},
#                     {'en': 'Kindred Bloodline'}
#                 ],
#                 'description': {
#                     'en': "Yeren, who dreams of being a vampire hunter, is unwittingly caught in the crossfire between a vampire girl and the Holy lands. As a temporary blood servant, he doesn't know what to do when the hatred and strife between them have been ongoing for thousands of years… This is a story about Lilo·I, the last vampire."},
#                 'isLocked': False,
#                 'links': {
#                     'mu': 'etgcwba',
#                     'raw': 'https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIzNjA5Nzk5OA==&action=getalbum&album_id=1906451382224650244&scene=173&sessionid=1628838356&enterid=1628838585&from_msgid=2650484487&from_itemidx=1&count=3&nolastread=1&uin=&key=&devicetype=Windows+10+x64&version=6309062f&lang=en&ascene=7&session_us=gh_9912f553adb7'},
#                 'originalLanguage': 'zh', 'lastVolume': None,
#                 'lastChapter': '', 'publicationDemographic': None,
#                 'status': 'ongoing', 'year': None,
#                 'contentRating': 'safe',
#                 'tags': [
#                     {'id': '07251805-a27e-4d59-b488-f0bfbec15168',
#                      'type': 'tag',
#                      'attributes': {'name': {'en': 'Thriller'},
#                                     'description': {}, 'group': 'genre',
#                                     'version': 1}, 'relationships': []},
#                     {'id': '2d1f5d56-a1e5-4d0d-a961-2193588b08ec',
#                      'type': 'tag', 'attributes': {'name': {'en': 'Loli'},
#                                                    'description': {},
#                                                    'group': 'theme',
#                                                    'version': 1},
#                      'relationships': []},
#                     {'id': '36fd93ea-e8b8-445e-b836-358f02b3d33d',
#                      'type': 'tag',
#                      'attributes': {'name': {'en': 'Monsters'},
#                                     'description': {}, 'group': 'theme',
#                                     'version': 1}, 'relationships': []},
#                     {'id': '391b0423-d847-456f-aff0-8b0cfc03066b',
#                      'type': 'tag', 'attributes': {'name': {'en': 'Action'},
#                                                    'description': {},
#                                                    'group': 'genre',
#                                                    'version': 1},
#                      'relationships': []},
#                     {'id': '3bb26d85-09d5-4d2e-880c-c34b974339e9',
#                      'type': 'tag', 'attributes': {'name': {'en': 'Ghosts'},
#                                                    'description': {},
#                                                    'group': 'theme',
#                                                    'version': 1},
#                      'relationships': []},
#                     {'id': '87cc87cd-a395-47af-b27a-93258283bbc6',
#                      'type': 'tag',
#                      'attributes': {'name': {'en': 'Adventure'},
#                                     'description': {}, 'group': 'genre',
#                                     'version': 1}, 'relationships': []},
#                     {'id': 'a1f53773-c69a-4ce5-8cab-fffcd90b1565',
#                      'type': 'tag', 'attributes': {'name': {'en': 'Magic'},
#                                                    'description': {},
#                                                    'group': 'theme',
#                                                    'version': 1},
#                      'relationships': []},
#                     {'id': 'cdad7e68-1419-41dd-bdce-27753074a640',
#                      'type': 'tag', 'attributes': {'name': {'en': 'Horror'},
#                                                    'description': {},
#                                                    'group': 'genre',
#                                                    'version': 1},
#                      'relationships': []},
#                     {'id': 'cdc58593-87dd-415e-bbc0-2ec27bf404cc',
#                      'type': 'tag', 'attributes': {'name': {'en': 'Fantasy'},
#                                                    'description': {},
#                                                    'group': 'genre',
#                                                    'version': 1},
#                      'relationships': []},
#                     {'id': 'd7d1730f-6eb0-4ba6-9437-602cac38664c',
#                      'type': 'tag',
#                      'attributes': {'name': {'en': 'Vampires'},
#                                     'description': {}, 'group': 'theme',
#                                     'version': 1}, 'relationships': []},
#                     {'id': 'eabc5b4c-6aff-42f3-b657-3e90cbd00b75',
#                      'type': 'tag',
#                      'attributes': {'name': {'en': 'Supernatural'},
#                                     'description': {}, 'group': 'theme',
#                                     'version': 1}, 'relationships': []},
#                     {'id': 'ee968100-4191-4968-93d3-f82d72be7e46',
#                      'type': 'tag', 'attributes': {'name': {'en': 'Mystery'},
#                                                    'description': {},
#                                                    'group': 'genre',
#                                                    'version': 1},
#                      'relationships': []},
#                     {'id': 'f5ba408b-0e7a-484d-8d49-4e9125ac96de',
#                      'type': 'tag',
#                      'attributes': {'name': {'en': 'Full Color'},
#                                     'description': {}, 'group': 'format',
#                                     'version': 1}, 'relationships': []}],
#                 'state': 'published',
#                 'chapterNumbersResetOnNewVolume': False,
#                 'createdAt': '2021-03-02T16:26:25+00:00',
#                 'updatedAt': '2024-01-16T17:00:34+00:00',
#                 'version': 12,
#                 'availableTranslatedLanguages': ['en'],
#                 'latestUploadedChapter': 'fe555074-2ed0-4f8d-8706-e56930e38e1f'},
#             'relationships': [
#                 {'id': 'e179c2e7-2689-4dcd-9ef7-19c4a84677ba',
#                  'type': 'author',
#                  'attributes': {'name': 'Aiou',
#                                 'imageUrl': None,
#                                 'biography': {},
#                                 'twitter': None, 'pixiv': None,
#                                 'melonBook': None,
#                                 'fanBox': None, 'booth': None,
#                                 'nicoVideo': None,
#                                 'skeb': None, 'fantia': None,
#                                 'tumblr': None,
#                                 'youtube': None, 'weibo': None,
#                                 'naver': None, 'website': None,
#                                 'createdAt': '2021-04-19T21:59:45+00:00',
#                                 'updatedAt': '2021-04-19T21:59:45+00:00',
#                                 'version': 1}},
#                 {'id': 'e179c2e7-2689-4dcd-9ef7-19c4a84677ba',
#                  'type': 'artist',
#                  'attributes': {'name': 'Aiou',
#                                 'imageUrl': None,
#                                 'biography': {},
#                                 'twitter': None, 'pixiv': None,
#                                 'melonBook': None,
#                                 'fanBox': None, 'booth': None,
#                                 'nicoVideo': None,
#                                 'skeb': None, 'fantia': None,
#                                 'tumblr': None,
#                                 'youtube': None, 'weibo': None,
#                                 'naver': None, 'website': None,
#                                 'createdAt': '2021-04-19T21:59:45+00:00',
#                                 'updatedAt': '2021-04-19T21:59:45+00:00',
#                                 'version': 1}},
#                 {'id': '48c71dc2-80b7-4b70-8d75-da1d4a96810f',
#                  'type': 'cover_art',
#                  'attributes': {'description': '',
#                                 'volume': '17',
#                                 'fileName': 'f9b4e32d-c99f-4f2f-8c5d-85b4bdc78b63.jpg',
#                                 'locale': 'zh',
#                                 'createdAt': '2024-01-15T04:55:06+00:00',
#                                 'updatedAt': '2024-01-15T04:55:06+00:00',
#                                 'version': 1}},
#                 {'id': '49e785f7-4213-4266-8b86-146bb55674be',
#                  'type': 'manga', 'related': 'prequel'}]}}
def load_extension():
    add_Extension(MangaDex())