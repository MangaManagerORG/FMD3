#!/usr/bin/python3
import logging
import pathlib
import threading
import tkinter
import tkinter as tk
from io import BytesIO
from tkinter import NW

import sv_ttk
from PIL import Image
import pygubu
from PIL import ImageTk
from urllib.request import urlopen

from FMD3.Core.database import DLDChapters
from FMD3.Models.Chapter import Chapter
from FMD3.Sources.SearchResult import SearchResult
from FMD3.api import get_chapters_from_serie_id, download_chapters

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "ui_test.ui"

from FMD3.Sources import get_sources_list, list_sources, load_sources, get_source, ISource


# load_sources()

def list_chapters_treeview(widget, chapter_list:list[DLDChapters], tags: tuple[str]):
    for chapter in chapter_list:
        widget.insert('', 'end', chapter.chapter_id, values=(chapter.title, chapter.volume, chapter.number), tags=tags)


def list_source_chapters_treeview(widget, chapter_list:list[Chapter], tags: tuple[str]):
    for chapter in chapter_list:
        widget.insert('', 'end', chapter.id, values=(chapter.title, chapter.volume, chapter.number), tags=tags)


def add_series_detail(series_detail_widget, data):
    series_detail_widget.delete('1.0', tkinter.END)
    series_detail_widget.tag_configure("bold", font="Helvetica 12 bold")

    series_detail_widget.insert("end", "Title:\n", "bold")

    series_detail_widget.insert("end", data.title)
    series_detail_widget.insert("end", "\n\n")
    series_detail_widget.insert("end", "Author(s):\n", "bold")
    series_detail_widget.insert("end", ",".join(data.authors))
    series_detail_widget.insert("end", "\n\n")

    series_detail_widget.insert("end", "Artist(s):\n", "bold")
    series_detail_widget.insert("end", ",".join(data.artists))
    series_detail_widget.insert("end", "\n\n")
    series_detail_widget.insert("end", "Genre(s):\n", "bold")
    series_detail_widget.insert("end", ",".join(data.genres))
    series_detail_widget.insert("end", "\n\n")
    series_detail_widget.insert("end", "Status:\n", "bold")
    series_detail_widget.insert("end", data.status)
    series_detail_widget.insert("end", "\n\n")
    series_detail_widget.insert("end", "Summary:\n", "bold")
    series_detail_widget.insert("end", data.description)


def getImageFromURL(url, controller):
    print('hai')
    try:
        response = controller.source.session.get(url)
        controller.mainwindow.series_detail_cover_image = ImageTk.PhotoImage(data=response.content)
        # notify controller that image has been downloaded
        # controller.mainwindow.event_generate("<<ImageLoaded>>")
        controller.on_series_detail_image_loaded()
    except Exception as e:
        logging.getLogger().exception("exception getting image from url")


class NuevoProyectoApp:
    @property
    def source(self) -> ISource:
        return get_source(self.builder.get_variable("selected_source_name").get())

    def __init__(self, master=None, translator=None):
        loaded_sources = list_sources()

        self.builder = builder = pygubu.Builder(translator)
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: tk.Tk = builder.get_object("tk1", master)
        builder.connect_callbacks(self)

        builder.get_object("source_selector_combobox").config(values=loaded_sources)
        self.mainwindow.state('zoomed')
        self.is_delayed_search = False
        self.search_results = {}

        cover_canvas = builder.get_object("series_detail_cover_canvas")

        self.series_detail_cover_image = None
        self.selected_series_id= None
        sv_ttk.use_dark_theme()

    def run(self):
        self.mainwindow.mainloop()

    def search_series(self, event):
        if not event.char:
            return
        ext = self.builder.get_variable("selected_source_name").get()
        if not ext:
            return
        if not self.is_delayed_search:
            self.is_delayed_search = True
            self.mainwindow.after(1500, self.delayed_search)

    def delayed_search(self, *_):
        # ext = self.builder.get_variable("selected_source_name").get()
        ext = "MangaDex"
        # query = self.builder.get_variable("query_stringvar").get()
        query = "tensei"
        if not query:
            return
        extension = get_source(ext)
        series = extension.find_series(query)
        tree = self.builder.get_object("series_result")
        tree.delete(*tree.get_children())
        for result in series:
            self.search_results[result.series_id] = result
            tree.insert('', 'end', result.series_id, text=result.title)

        self.is_delayed_search = False

    def select_query_result(self, event):
        search_result: SearchResult = self.search_results.get(event.widget.selection()[0])
        data = self.source.get_info(search_result.series_id)
        self.selected_series_id = search_result.series_id
        series_detail_widget = self.builder.get_object("series_detail")

        add_series_detail(series_detail_widget, data)

        chapters_treeview = self.builder.get_object("selected_series_chapter_treeview")
        chapters_treeview.tag_configure('downloaded', background='lime')
        chapters_treeview.tag_configure('not_downloaded', background='grey')
        chapters_treeview.delete(*chapters_treeview.get_children())

        if dld_chapters := get_chapters_from_serie_id(search_result.series_id):
            last_in_db = max(dld_chapters,key=lambda x:x.number)
            list_chapters_treeview(chapters_treeview,dld_chapters,("downloaded",))
            chapters = self.source.get_new_chapters(search_result.series_id,last_in_db.number)
            list_source_chapters_treeview(chapters_treeview, chapters, ("not_downloaded",))
        else:
            chapters = self.source.get_chapters(search_result.series_id)
            list_source_chapters_treeview(chapters_treeview, chapters, ("not_downloaded",))

        # threading.Thread(target=getImageFromURL, args=(data.cover_url, self)).start()
        self.mainwindow.update()
        response = self.source.session.get(data.cover_url)
        image_ = BytesIO(response.content)
        image = Image.open(image_)
        image = image.resize((90, 160), Image.NEAREST)
        self.mainwindow.series_detail_cover_image = ImageTk.PhotoImage(image)
        print("image_loaded")

        canvas = self.builder.get_object("series_detail_cover_canvas")
        canvas.create_image(0, 0, image=self.mainwindow.series_detail_cover_image, anchor=NW)

        # canvas.itemconfig(canvas.image_id, image=self.series_detail_cover_image, state="normal")
        # canvas.config(image=self.series_detail_cover_image)
        ...

    def download_selected_chapters(self):
        chapters_treeview = self.builder.get_object("selected_series_chapter_treeview")
        to_download_ids = chapters_treeview.selection()
        to_download_series = self.selected_series_id
        download_chapters(self.source.NAME,to_download_series,to_download_ids)


if __name__ == "__main__":
    app = NuevoProyectoApp()
    app.run()
