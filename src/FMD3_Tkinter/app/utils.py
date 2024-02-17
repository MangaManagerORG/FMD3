from datetime import datetime
from pathlib import Path
from tkinter import END
from FMD3.api.series import get_series_folder_name
from FMD3_Tkinter import api


def add_detail_entry(widget, data, title, data_key, tag=""):
    """
    Helper function to insert the formatted text from the data into the :class:`customtkinter.CTKTextbox`
    :param widget: :class:`customtkinter.CTKTextbox`
    :param data: dict
    :param title: str
    :param data_key: str
    :param tag: str
    :return:
    """
    widget.insert("end", f"{title}:\n", "bold" + tag)
    widget.insert("end", f"{data[data_key]}\n\n")


def add_detail_entry_array(widget, data, title, data_key, tag=""):
    """
    Helper function to insert a list from the data in the :class:`customtkinter.CTkTextbox`
    :param widget:
    :param data:
    :param title:
    :param data_key:
    :param tag:
    :return:
    """
    widget.insert("end", f"{title}:\n", "bold" + tag)
    value = data[data_key]
    if value:
        data_ = ','.join(value)
    else:
        data_ = ""
    widget.insert("end", f"{data_}\n\n")


def add_series_detail(series_detail_widget, data: dict):
    """
    Unlocks the :class:`customtkinter.CTkTextbox` and fills it with the data from the series
    :param series_detail_widget: :class:`customtkinter.CTkTextbox`
    :param data: dict containing: ["title","authors","artists","generes,"status","description"]
    :return:
    """
    series_detail_widget.configure(state="normal")
    series_detail_widget.delete('1.0', END)

    add_detail_entry(series_detail_widget, data, "Title", "title", tag="")
    add_detail_entry_array(series_detail_widget, data, "Author(s)", "authors", tag="")
    add_detail_entry_array(series_detail_widget, data, "Artist(s)", "artists", tag="")
    add_detail_entry_array(series_detail_widget, data, "Genre(s)", "genres", tag="")
    add_detail_entry(series_detail_widget, data, "Status", "status", tag="")
    add_detail_entry(series_detail_widget, data, "Summary", "description", tag="")
    series_detail_widget.configure(state="disabled")


def list_chapters_treeview(widget, chapter_list: list, tags: tuple[str]):
    for chapter in chapter_list:
        widget.insert('', 'end', chapter.get("chapter_id"),
                      values=(chapter.get("volume"), chapter.get("number"), chapter.get("title")), tags=tags)



def get_sanitized_download(parent,website=None, manga=None, author=None, artist=None):
    return Path(parent,
                        get_series_folder_name(website=website, manga=manga, author=author, artist=artist))

def _str_to_datetime(string):
    return datetime.strptime(string, "%Y-%m-%dT%H:%M:%S" if "T" in string else "%Y-%m-%d %H:%M:%S")

