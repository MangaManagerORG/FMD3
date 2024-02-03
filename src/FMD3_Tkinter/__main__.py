import json
import pathlib
import tkinter as tk
from tkinter import ttk

import pygubu
from FMD3_Tkinter.app import App
from FMD3_Tkinter.api import get_series_info
from FMD3_Tkinter.api import get_settings
from FMD3_Tkinter.api import get_sources
from FMD3_Tkinter.api import update_settings_save_to as update_save_to

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "ui_test.ui"

sources = get_sources()


class Source_():
    def __init__(self, id, name):
        self.id_ = id
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class TkinterUI(App):
    def test(self, *args):
        print("asdas")

    def do_popup(self, event):
        m = self.builder.get_object("fav_treeview_ctx_menu")

        try:
            selected_item = self.favourites_treeview.identify_row(event.y)
            if selected_item in self.fav_tree_loaded_parents:
                self.favourites_treeview.selection_set(selected_item)
                # m.selection = self.favourites_treeview.set(self.favourites_treeview.identify_row(event.y))
                # m.post(event.x_root, event.y_root)
                m.tk_popup(event.x_root, event.y_root)
        finally:
            m.grab_release()

    def show_edit_save_to(self, *args):
        # "series_destination_path_edit"
        # "top_level_edit_save_to"
        self.builder.get_object('dialog1', self.mainwindow).run()
        self.builder.connect_callbacks(self)
        series_id = self.favourites_treeview.selection()
        vals = self.favourites_treeview.item(series_id, "values")

        toplevel_entry_val = self.builder.get_variable("series_destination_path_edit")
        toplevel_entry_val.set(vals[2])
        # top_level.deiconify()

    def update_series_destination_path_submit(self, *args):
        series_id = self.favourites_treeview.selection()[0]
        vals = list(self.favourites_treeview.item(series_id, "values"))

        toplevel_entry_val = self.builder.get_variable("series_destination_path_edit")
        vals[2] = toplevel_entry_val.get()
        self.favourites_treeview.item(series_id, values=vals)
        update_save_to(series_id, toplevel_entry_val.get())
        print("edited")

        self.close_series_destination_path_submit()

    def close_series_destination_path_submit(self, *args):
        top_level = self.builder.get_object('dialog1')
        toplevel_entry_val = self.builder.get_variable("series_destination_path_edit")
        toplevel_entry_val.set(None)
        top_level.close()

    def __init__(self, master=None, translator=None):

        self.settings = json.loads(get_settings())

        self.builder = builder = pygubu.Builder(translator)
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: tk.Tk = builder.get_object("tk1", master)
        self.favourites_treeview = self.builder.get_object("favourites_treeview")
        self.favourites_treeview.bind("<Button-3>", self.do_popup)
        self.favourites_treeview: ttk.Treeview
        self.favourites_treeview.focus()

        self.builder.get_object("fav_treeview_ctx_menu", master)
        # self.builder.get_object("command2")

        # top2 = tk.Toplevel(self.mainwindow)

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
        self.mainwindow.state('zoomed')

        self.track_setting("default_downloads_path")
        # self.track_checkbox("replace_unicode_char_checkbox","replace_unicode_char_with_entry")
        self.track_setting("replace_unicode", "replace_unicode_char_with_entry")
        self.track_setting("replace_unicode_with")

        self.track_setting("generate_series_folder", "manga_folder_name_entry")
        self.track_setting("series_folder_name")

        # self.track_setting("remove_manga_name_from_chapter_name")
        self.track_setting("chapter_name")

        self.track_setting("rename_chapter_digits_volume", "rename_volume_digits_spinbox")
        self.track_setting("rename_chapter_digits_chapter", "rename_chapter_digits_spinbox")
        self.track_setting("rename_chapter_digits_volume_value")
        self.track_setting("rename_chapter_digits_chapter_value")

        self.settings_libraries = {}
        self.track_setting("default_downloads_path")  # ,"settings_def_lib_combo")

        # Library selection field
        default_series_downloads_path = builder.get_variable("default_series_downloads_path")
        default_series_downloads_path.trace_add("write", self.series_update_final_dest)


        # Series field
        series_destination_path = builder.get_variable("series_destination_path")
        series_destination_path.trace_add("write", self.series_update_final_dest)
        super().__init__()
        self.settings_load_save_to_treeview_from_settings()

        # Library selection field set default
        default_series_downloads_path.set(self.settings["Core"].get("default_downloads_path", None)["value"])



    def on_source_selected(self, *_):

        combo = self.builder.get_object("source_selector_combobox")
        selected_index = combo.current()
        source = sources[selected_index]
        self.selected_source_id = source.get("id")
        # selected_value = values[selected_index][1]  # Extract the second element of the tuple

    # Cross tabs methods
    def show_selected_in_series_tab(self, *_):
        tree = self.builder.get_object("favourites_treeview")

        if tree.selection():
            series_id = tree.selection()[0]
            values = tree.item(series_id, "values")
            if not self.selected_source_id:
                self.selected_source_id = values[7]
            data = get_series_info(values[7], tree.selection()[0])
            if data:
                self.selected_series_id = series_id
                series_result_tree = self.builder.get_object("series_result")
                series_result_tree.delete(*series_result_tree.get_children())
                self.load_queried_data(series_id, data)
                self.builder.get_object("notebook_widget").select(1)

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = TkinterUI()
    app.run()
