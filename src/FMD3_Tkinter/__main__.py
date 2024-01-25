import pathlib
import tkinter as tk
import pygubu

from FMD3.api import get_sources
from FMD3_Tkinter.app import App

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "ui_test.ui"

sources = get_sources()
class Source_():
    def __init__(self,id,name):
        self.id_ = id
        self.name = name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name

class TkinterUI(App):

    def __init__(self, master=None, translator=None):

        self.builder = builder = pygubu.Builder(translator)
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: tk.Tk = builder.get_object("tk1", master)
        self.favourites_treeview = self.builder.get_object("favourites_treeview")
        builder.connect_callbacks(self)
        s = get_sources()
        builder.get_object("source_selector_combobox").config(values=[s["name"] for s in sources])

        self.selected_source_id = None
        self.search_results = {}
        self.is_delayed_search = False
        self.builder.get_object("series_detail").tag_configure("bold", font="Helvetica 12 bold")
        chapters_treeview = self.builder.get_object("selected_series_chapter_treeview")
        chapters_treeview.tag_configure('downloaded', background='lime')
        chapters_treeview.tag_configure('not_downloaded', background='grey')
        self.series_detail_cover_image = None
        super().__init__()

    def on_source_selected(self,*_):

        combo = self.builder.get_object("source_selector_combobox")
        selected_index = combo.current()
        source = sources[selected_index]
        self.selected_source_id = source.get("id")
        # selected_value = values[selected_index][1]  # Extract the second element of the tuple
    def run(self):
        self.mainwindow.mainloop()
if __name__ == "__main__":
    app = TkinterUI()
    app.run()
