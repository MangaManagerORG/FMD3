"""
Module with helping functions such as parsing filename templates
"""

from FMD3.Models.Chapter import Chapter


def make_filename(chapter: Chapter, series_filename):
    vol_str = f" Vol.{chapter.volume}" if chapter.volume else ""
    ch_str = f" Ch.{chapter.number}"
    return series_filename + vol_str + ch_str + ".cbz"
    # add metadata:
