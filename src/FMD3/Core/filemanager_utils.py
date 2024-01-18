from FMD3.Models.Chapter import Chapter


def get_output_folder(path):
    """
    Hook to provide full output folder customization.
    :param path: The predefined root path. Could be a library root.
    :return:
    """
    return path


def make_filename(chapter: Chapter, series_filename)
    vol_str = f" Vol.{chapter.volume}" if chapter.volume else ""
    ch_str = f" Ch.{chapter.number}"
    return series_filename + vol_str + ch_str + ".cbz"
    # add metadata:
