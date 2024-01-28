import logging

groups = [
    "4f1de6a2-f0c5-4ac5-bce5-02c7dbb67deb",  # "MangaPlus",
    "8d8ecf83-8d42-4f8c-add8-60963f9f28d9",  # "Comikey",
    "5fed0576-8b94-4f9a-b6a7-08eecd69800d",  # "Azuki Manga",
    "caa63201-4a17-4b7f-95ff-ed884a2b7e60",  # "INKR Comics",
    "4ba19c33-6cc2-43ff-b157-5501b057fce7",  # "J-Novel Club"
]


def IgnoreChaptersByGroupId(id) -> bool:
    return id in groups


def get_demographic(demograhic):
    demographics = {
        "shounen": "Shounen",
        "shoujo": "Shoujo",
        "seinen": "Seinen",
        "josei": "Josei"
    }
    if demograhic in demographics:
        return demographics[demograhic]
    return None


langs = {
    "ar": "Arabic",
    "bn": "Bengali",
    "bg": "Bulgarian",
    "my": "Burmese",
    "ca": "Catalan",
    "zh": "Chinese (Simp)",
    "zh-hk": "Chinese (Trad)",
    "cs": "Czech",
    "da": "Danish",
    "nl": "Dutch",
    "en": "English",
    "fi": "Finnish",
    "fr": "French",
    "de": "German",
    "el": "Greek",
    "he": "Hebrew",
    "hi": "Hindi",
    "hu": "Hungarian",
    "id": "Indonesian",
    "it": "Italian",
    "ja": "Japanese",
    "ko": "Korean",
    "lt": "Lithuanian",
    "ms": "Malay",
    "mn": "Mongolian",
    "ne": "Nepali",
    "no": "Norwegian",
    "NULL": "Other",
    "fa": "Persian",
    "pl": "Polish",
    "pt-br": "Portuguese (Br)",
    "pt": "Portuguese (Pt)",
    "ro": "Romanian",
    "ru": "Russian",
    "sh": "Serbo-Croatian",
    "es": "Spanish (Es)",
    "es-la": "Spanish (LATAM)",
    "sv": "Swedish",
    "tl": "Tagalog",
    "th": "Thai",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "vi": "Vietnamese"
}

genres = {
    "1": "4-koma",
    "2": "Action",
    "3": "Adventure",
    "4": "Award Winning",
    "5": "Comedy",
    "6": "Cooking",
    "7": "Doujinshi",
    "8": "Drama",
    "9": "Ecchi",
    "10": "Fantasy",
    "11": "Gyaru",
    "12": "Harem",
    "13": "Historical",
    "14": "Horror",
    "15": "Josei",
    "16": "Martial Arts",
    "17": "Mecha",
    "18": "Medical",
    "19": "Music",
    "20": "Mystery",
    "21": "Oneshot",
    "22": "Psychological",
    "23": "Romance",
    "24": "School Life",
    "25": "Sci-Fi",
    "26": "Seinen",
    "27": "Shoujo",
    "28": "Shoujo Ai",
    "29": "Shounen",
    "30": "Shounen Ai",
    "31": "Slice of Life",
    "32": "Smut",
    "33": "Sports",
    "34": "Supernatural",
    "35": "Tragedy",
    "36": "Long Strip",
    "37": "Yaoi",
    "38": "Yuri",
    "39": "[no chapters]",
    "40": "Video Games",
    "41": "Isekai",
    "42": "Adaptation",
    "43": "Anthology",
    "44": "Web Comic",
    "45": "Full Color",
    "46": "User Created",
    "47": "Official Colored",
    "48": "Fan Colored",
    "49": "Gore",
    "50": "Sexual Violence",
    "51": "Crime",
    "52": "Magical Girls",
    "53": "Philosophical",
    "54": "Superhero",
    "55": "Thriller",
    "56": "Wuxia",
    "57": "Aliens",
    "58": "Animals",
    "59": "Crossdressing",
    "60": "Demons",
    "61": "Delinquents",
    "62": "Genderswap",
    "63": "Ghosts",
    "64": "Monster Girls",
    "65": "Loli",
    "66": "Magic",
    "67": "Military",
    "68": "Monsters",
    "69": "Ninja",
    "70": "Office Workers",
    "71": "Police",
    "72": "Post-Apocalyptic",
    "73": "Reincarnation",
    "74": "Reverse Harem",
    "75": "Samurai",
    "76": "Shota",
    "77": "Survival",
    "78": "Time Travel",
    "79": "Vampires",
    "80": "Traditional Games",
    "81": "Virtual Reality",
    "82": "Zombies",
    "83": "Incest",
    "84": "Mafia",
    "85": "Villainess"
}


def get_lang(lang):
    if lang in langs:
        return langs[lang]
    return "Unknown"


def get_langs():
    return langs


def get_rating(rating):
    if not rating:
        return None
    return str(rating).capitalize()


def check_empty_chapters(chapter_attrs):
    """
    Ignore chapter if it has no pages or an external link


    :return True if valid -> has pages and no external link
    """
    return chapter_attrs["pages"] > 0 and chapter_attrs["externalUrl"] is None


def check_group_id(relationships: filter):
    """
    Check if the group that released the chapter is on the built-in ignore list, otherwise skip the chapter

    :return True if there are no blocked group"""
    for relation in relationships:
        if relation["id"] in groups:
            return False
    return True


