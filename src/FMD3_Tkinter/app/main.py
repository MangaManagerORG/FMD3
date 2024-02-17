#!/usr/bin/python3
import pathlib

from customtkinter import CTkComboBox, CTkOptionMenu

from FMD3_Tkinter import api
from FMD3_Tkinter.app.baseui import BaseUi
from FMD3_Tkinter.app.utils import add_series_detail, list_chapters_treeview, get_sanitized_download, _str_to_datetime

sources = api.get_sources()


class Fmd3App(BaseUi):
    def __init__(self, master=None, translator=None):




        super().__init__(master, translator)
        self.selected_series_chapter_treeview = self.builder.get_object("selected_series_chapter_treeview")
        self.series_output_save_to_entry = self.builder.get_object("series_output_save_to_entry")
        self.selected_series_chapter_treeview = self.builder.get_object("selected_series_chapter_treeview")
        self.frame_test_image = self.builder.get_object("frame_test_image")
        self.settings_default_series_library_combo = self.builder.get_object("settings_def_series_lib_combobox")
        self.source_selector_optionmenu: CTkOptionMenu = self.builder.get_object("source_selector_optionmenu")
        self.favourites_treeview = self.builder.get_object("favourites_treeview")
        self.builder.connect_callbacks(self)

        self.default_series_downloads_path.set("No default lib selected")

        #
        # Add binds
        #

        # Search stuff
        self.is_delayed_search = False  # Adds delay so function is not called on each keystroke
        self.search_results = {}  # Stores the returned series by api
        self.query_stringvar.trace_add("write", self.search_series)  # Triggers search on each keystroke

        # load sources
        self.selected_source_id = None
        self.source_selector_optionmenu.configure(values=[s["name"] for s in sources])

        # Favourites stuff
        favourites_treeview: type[""]
        builder: type[""]
        self.fav_tree_loaded_parents = {}
        self.favourites_treeview.tag_bind('lazy', '<<TreeviewOpen>>', self.child_opened_fav_treeview)
        self.favourites_treeview.bind('<Button-1>', self.child_opened_fav_treeview)
        self.favourites_treeview.tag_configure('favourites_child_chapters', background='#B6B7B7')
        self.load_favourites()
        self._detached_fav_filter = set()

    def run(self):
        self.mainwindow.mainloop()

    def on_source_selected(self,selected_value,*_):
        combo = self.builder.get_object("source_selector_optionmenu")
        source = list(filter(lambda s: s["name"] == selected_value, sources))
        if not source:
            self.selected_source_id = None
        else:
            self.selected_source_id = source[0]["id"]
            # selected_value = values[selected_index][1]  # Extract the second element of the tuple

    def on_series_result_selected(self,event):
        search_result = self.search_results.get(event.widget.selection()[0])
        series_id = search_result.get("series_id")
        data = api.get_series_info(self.selected_source_id, series_id)
        self._get_series_info(data)

    def search_series(self, _, new_value, *__):
        ext = self.selected_source_id
        if not ext:
            return
        if not self.is_delayed_search:
            self.is_delayed_search = True
            self.mainwindow.after(500, self.delayed_search)

    def delayed_search(self, *_):
        # ext = self.builder.get_variable("selected_source_name").get()
        source_id = self.selected_source_id
        query = self.builder.get_variable("query_stringvar").get()
        # query = "tensei"
        if not query:
            return

        series_list = api.query_series(self.selected_source_id, query)

        tree = self.builder.get_object("series_result")
        tree.delete(*tree.get_children())
        for result in series_list:
            self.search_results[result.get("series_id")] = result
            tree.insert('', 'end', result.get("series_id"), text=result.get("title"))

        self.is_delayed_search = False


    def series_tab_search_by_url(self):
        if series_url := self.series_browser_url_entry_var.get():
            data = api.get_series_from_url(series_url)
            self._get_series_info(data)

    def settings_load_libs_from_treeview(self, current_value):
        libs = self.settings_libraries
        self.builder.get_object("settings_def_lib_combo")['values'] = list(libs)
        self.builder.get_object("settings_def_series_lib_combo")['values'] = list(libs)

    def add_library_to_treeview(self):
        path = self.settings_lib_path_entry.get()
        alias = self.settings_lib_alias_entry.get()
        self.settings_libraries[self.settings_lib_alias_entry.get()] = path

        tree = self.builder.get_object("settings_libraries_treeview")

        tree.insert('', 'end', path, values=(alias, path))
        self.settings["Core"].get("libraries_alias_paths_list")["value"].append({"alias": alias, "path": path})

        # Clear entries
        self.settings_lib_path_entry.set("")
        self.settings_lib_alias_entry.set("")

    def fav_sort_date_added(self):
        tv = self.favourites_treeview
        col = "dateadded"
        reverse = True
        l = [
            (_str_to_datetime(tv.set(k, col)), k)
            for k in tv.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

    def child_opened_fav_treeview(self, event=None):
        series_id = self.favourites_treeview.focus()
        if not series_id:
            return
        # Check if the item has been loaded
        if not self.fav_tree_loaded_parents.get(series_id, False):
            # Load the children of the parent item
            self.load_children(series_id)
            # Mark the parent as loaded
            self.fav_tree_loaded_parents[series_id] = True

    def load_children(self, parent_id):
        # Simulate loading children from a data source
        for chapter in sorted(api.get_chapters(parent_id), key=lambda x: x.get("number")):
            self.favourites_treeview.insert(parent_id, 'end', text=chapter.get("title") or "",
                                            values=(
                                                f'Ch.{chapter["number"]} Vol.{chapter["volume"]}', "",
                                                chapter.get("path"),
                                                chapter.get("download_date"),
                                                chapter.get("status"), "", "", ""),
                                            tags=("favourites_child_chapters",))

    def _get_series_info(self, data):
        if not data:
            return
        series_id = data["id"]
        self.selected_source_id = data.get("source_id")
        self.selected_series_id = series_id
        add_series_detail(self.builder.get_object("series_detail"), data)
        self.load_queried_data(series_id, data)

    def load_queried_data(self, series_id, data):
        self.selected_series_chapter_treeview.delete(*self.selected_series_chapter_treeview.get_children())
        if dld_chapters := api.get_chapters(series_id):
            last_in_db = max(dld_chapters, key=lambda x: x["number"])
            list_chapters_treeview(self.selected_series_chapter_treeview, dld_chapters, ("downloaded",))
            chapters = api.get_source_chapters(self.selected_source_id, series_id, last_in_db.get("number"))
            list_chapters_treeview(self.selected_series_chapter_treeview, chapters, ("not_downloaded",))
        else:
            chapters = api.get_source_chapters(data["source_id"], series_id)
            list_chapters_treeview(self.selected_series_chapter_treeview, chapters, ("not_downloaded",))
        self.frame_test_image.load_website(data.get("cover_url"))
        sanitized_download = get_sanitized_download(self.settings["Core"].get("default_download_path", "")["value"],
                                                    manga=data.get("title"))
        if data.get("save_to", None) is not None:
            self.series_output_save_to_entry.configure(state="disabled")
            self.settings_default_series_library_combo.configure(state="disabled")
            self.series_final_download_dest.set(data.get("save_to"))
            # self.series_destination_path.set(data.get("save_to"))
        else:
            self.series_output_save_to_entry.configure(state="normal")
            self.settings_default_series_library_combo.configure(state="readonly")
            self.series_destination_path.set(sanitized_download)

    def load_favourites(self, series_list=api.get_series(sort="dateadded", order="desc")):
        for series in series_list:
            if series.get("series_id") not in self.fav_tree_loaded_parents:
                source = api.get_source(source_id=series.get("source_id"))
                if source:
                    source_name = source.get("name")
                else:
                    source_name = "Unknown(Not Loaded)"
                item_id = self.favourites_treeview.insert('', 'end', series.get("series_id"), text=series.get("title"),
                                                          values=(series.get("max_chapter"),
                                                                  source_name,
                                                                  series.get("save_to"),
                                                                  series.get("dateadded"),
                                                                  series.get("status"),
                                                                  series.get("datelastchecked"),
                                                                  series.get("datelastupdated"),
                                                                  series.get("source_id")))
                # self.favourites_treeview.insert('', 'end', f"{series.series_id}.chapters", values=(series.title, series.currentchapter))
                self.fav_tree_loaded_parents[item_id] = False
        self.fav_sort_date_added()


if __name__ == "__main__":
    app = Fmd3App()
    app.run()
