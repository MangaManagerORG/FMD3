#!/usr/bin/python3
import asyncio
import logging
import pathlib
import time
from threading import Thread
from typing import Literal

from ttkwidgets import CheckboxTreeview

from customtkinter import CTkComboBox, CTkOptionMenu, CTkEntry

from FMD3_Tkinter import api
from FMD3_Tkinter.app.baseui import BaseUi
from FMD3_Tkinter.app.utils import add_series_detail, list_chapters_treeview, get_sanitized_download, _str_to_datetime, \
    throttle
from pathlib import Path
sources = api.get_sources()
assets_path = Path(Path(__file__).parent.parent, "assets")
logger = logging.getLogger(__name__)
class Fmd3App(BaseUi):
    def __init__(self, master=None, translator=None):
        super().__init__(master, translator)
        self.series_chapterlist_treeview = self.builder.get_object("series_chapterlist_treeview")
        self.series_output_save_to_entry = self.builder.get_object("series_output_save_to_entry")
        self.series_chapterlist_treeview = self.builder.get_object("series_chapterlist_treeview")
        self.frame_test_image = self.builder.get_object("frame_test_image")
        self.settings_default_series_library_combo = self.builder.get_object("settings_def_series_lib_combobox")
        self.source_selector_optionmenu: CTkOptionMenu = self.builder.get_object("source_selector_optionmenu")
        self.favourites_treeview = self.builder.get_object("favourites_treeview")
        self.builder.connect_callbacks(self)

        self.default_series_downloads_path.set("No default lib selected")
        self.series_info_frame = self.builder.get_object("series_info_frame")

        # self.loading_overlay.place_forget()

        # self.loading_overlay.lower()

        #
        # Add binds
        #
        # Search stuff
        self.is_delayed_search = False  # Adds delay so function is not called on each keystroke
        self.search_results = {}  # Stores
        self.series_search_series_entry = self.builder.get_object("series_search_series_entry")
        self.series_result = self.builder.get_object("series_result")
        self.series_details = self.builder.get_object("series_details")


        # self.series_search_series_entry.bind("<Key>",self.search_series)
        # self.series_search_series_entry.bind("<Return>", self.search_series)
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
        self.search_delay = False
        self.last_search_selected_item = None

    def loading(self,state):
        if state:
            self.mainwindow.config(cursor="wait")
        else:
            self.mainwindow.config(cursor="")


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

    def search_series(self,*_):
        logging.debug("search called")
        value = self.query_stringvar.get()
        if not value or len(value) <= 2:
            return

        ext = self.selected_source_id
        if not ext:
            return
        source_id = self.selected_source_id

        # Thread(target=self.fetch_series_by_name, args=(source_id,value,data)).join()
        # data = self.fetch_series_by_name(source_id,value)
        self.fetch_series_by_name(source_id, value)
        # self.fetch_series_by_name_callback(None)

    @throttle(2.3)
    def fetch_series_by_name(self,source_id, query):
        self.series_result.delete(*self.series_result.get_children())
        self.task_manager.submit(api.query_series, self.fetch_series_by_name_callback, source_id, query)

    def fetch_series_by_name_callback(self,future):
        self.mainwindow.after(0, self.fetch_series_by_name_callback_after, future.result())
    def fetch_series_by_name_callback_after(self,result):
        # a = [{'series_id': '3fc308c9-4b00-4dc3-943e-1f39242bc708', 'title': 'Overgeared', 'cover_url': 'https://uploads.mangadex.org/covers/3fc308c9-4b00-4dc3-943e-1f39242bc708/2af0c6f7-cd3d-4c59-afee-a8ff471e0561.jpg'}, {'series_id': '30f3ac69-21b6-45ad-a110-d011b7aaadaa', 'title': 'Tonikaku Kawaii', 'cover_url': 'https://uploads.mangadex.org/covers/30f3ac69-21b6-45ad-a110-d011b7aaadaa/b6807299-6031-4a7a-ba9f-ba0b302f7742.jpg'}, {'series_id': '80dbce9d-92a8-4a19-8bd5-b1727dc0f6c8', 'title': 'Choukadou Girls', 'cover_url': 'https://uploads.mangadex.org/covers/80dbce9d-92a8-4a19-8bd5-b1727dc0f6c8/d533a948-96a6-48eb-a7ed-cf60cef66c39.jpg'}, {'series_id': '11b74211-f4c0-4f08-b5a4-c491da0d0c0b', 'title': 'Choujin X', 'cover_url': 'https://uploads.mangadex.org/covers/11b74211-f4c0-4f08-b5a4-c491da0d0c0b/d1253987-3fb4-4d6d-ae60-1f3e9d0dfd36.jpg'}, {'series_id': 'ca3d5247-82a5-48b9-a921-7079bb9d314b', 'title': 'Muv-Luv Alternative: Tsukikage wa Yamiyo ni Arite', 'cover_url': 'https://uploads.mangadex.org/covers/ca3d5247-82a5-48b9-a921-7079bb9d314b/83aed29b-37aa-4b43-9250-083e29a81764.jpg'}, {'series_id': '6ba37a68-bc82-4030-b550-899ecd9446af', 'title': 'Ring My Bell!', 'cover_url': 'https://uploads.mangadex.org/covers/6ba37a68-bc82-4030-b550-899ecd9446af/813e99a3-2bd3-475d-8534-f374ea0100d5.jpg'}, {'series_id': 'b78bbae9-f525-45d5-b832-f15dcbe1c489', 'title': "A Transmigrated Warden's Battle for Redemption", 'cover_url': 'https://uploads.mangadex.org/covers/b78bbae9-f525-45d5-b832-f15dcbe1c489/4b86560b-8037-4790-a6f9-a44e67172bc3.png'}, {'series_id': 'ac4e2459-d995-45ae-8421-4c4cf4a87770', 'title': 'Overlord', 'cover_url': 'https://uploads.mangadex.org/covers/ac4e2459-d995-45ae-8421-4c4cf4a87770/ac86c0df-e801-4245-977f-5f5e44746198.jpg'}, {'series_id': '40de5fa6-1268-4445-aeb9-5e22aa82d6b0', 'title': 'Oshiete Kudasai, Fujishima-san!', 'cover_url': 'https://uploads.mangadex.org/covers/40de5fa6-1268-4445-aeb9-5e22aa82d6b0/46891e30-f392-4f2c-9cc2-e862d297fd03.jpg'}, {'series_id': 'd1fa8ce7-ad9d-475d-9311-2a850b1f3336', 'title': 'Sekai wa Owattemo Ikirutte Tanoshii', 'cover_url': 'https://uploads.mangadex.org/covers/d1fa8ce7-ad9d-475d-9311-2a850b1f3336/70b7e691-c1c2-4898-8f35-b80c6c99645d.jpg'}]
        # self.mainwindow.after(10, self.update_search_list, a)
        self.update_search_list(result)
    def update_search_list(self,series_list):

        self.search_delay = False
        logging.debug("updating search list")
        tree = self.builder.get_object("series_result")
        new_ids = [series["series_id"] for series in series_list]
        old_ids = [series_id for series_id in tree.get_children() if series_id not in new_ids]
        kept_ids = [series_id for series_id in tree.get_children() if series_id in new_ids]
        # tree.update()
        # tree.delete(*old_ids)
        # tree.update()
        # time.sleep(0.2)
        for result in series_list:
            if result["series_id"] in kept_ids:
                continue
            self.search_results[result.get("series_id")] = result
            tree.insert('', 'end', result.get("series_id"), text=result.get("title"))
        self.is_delayed_search = False
        self.loading(False)

    def series_tab_search_by_url(self):
        if series_url := self.series_browser_url_entry_var.get():
            data = api.get_series_from_url(series_url)
            self._get_series_info(data)

    def on_series_result_selected(self,event):
        search_result = self.search_results.get(event.widget.selection()[0])
        series_id = search_result.get("series_id")
        if self.last_search_selected_item:
            if series_id == self.last_search_selected_item:
                return
        self.last_search_selected_item = series_id
        self.task_manager.submit(self._get_series_info, self._get_series_info_from_data_callback, series_id)

    def _get_series_info(self,series_id):
        return api.get_series_info(self.selected_source_id, series_id)

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
            self._load_children(series_id)
            # Mark the parent as loaded
            self.fav_tree_loaded_parents[series_id] = True

    def _load_children(self, parent_id):
        # Simulate loading children from a data source
        for chapter in sorted(api.get_chapters(parent_id), key=lambda x: x.get("number")):
            self.favourites_treeview.insert(parent_id, 'end', text=chapter.get("title") or "",
                                            values=(
                                                f'Ch.{chapter["number"]} Vol.{chapter["volume"]}', "",
                                                chapter.get("path"),
                                                chapter.get("download_date"),
                                                chapter.get("status"), "", "", ""),
                                            tags=("favourites_child_chapters",))


    def _get_series_info_from_data_callback(self,future):
        self.mainwindow.after(0, self._get_series_info_from_data,future.result())
    def _get_series_info_from_data(self, data):
        if not data:
            return
        series_id = data["id"]
        self.selected_source_id = data.get("source_id")
        self.selected_series_id = series_id
        add_series_detail(self.series_details, data)
        self.mainwindow.update_idletasks()

        self.set_series_library_output_path(data)
        self.task_manager.submit(self.frame_test_image.load_website, None, data.get("cover_url"))
        self.series_chapterlist_treeview.delete(*self.series_chapterlist_treeview.get_children())
        self.task_manager.submit(self.load_queried_chapters, None, series_id,data)

    def load_queried_chapters(self, series_id, data):
        has_chapters = False
        if dld_chapters := api.get_chapters(series_id):
            has_chapters = True
            self.no_chapters_frame.lower()
            last_in_db = max(dld_chapters, key=lambda x: x["number"])
            list_chapters_treeview(self.series_chapterlist_treeview, dld_chapters, ("downloaded",))
            args = (self.selected_source_id, series_id, last_in_db.get("number"))
        else:
            args = (data["source_id"], series_id)
        chapters = api.get_source_chapters(*args)
        if chapters:
            has_chapters = True
            list_chapters_treeview(self.series_chapterlist_treeview, chapters, ("not_downloaded",))

        if has_chapters:
            self.no_chapters_frame.lower()
        else:
            self.no_chapters_frame.lift()

    def set_series_library_output_path(self,data):
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

    def series_on_menu_select(self,action,argument):
        match action:
            case "Select":
                self._cb_series_on_select(argument)
            case "Download":
                self._cb_series_on_download(argument)
            case "Favourite":
                self._cb_series_on_download(argument)

    def _cb_series_on_select(self, value):
        tree: CheckboxTreeview = self.builder.get_object("series_chapterlist_treeview")

        if value == "None":
            tree.uncheck_all()
        if value == "All":
            tree.check_all()

    def _cb_series_on_download(self, value):
        ...

    def _cb_series_on_fav(self, value):
        ...


if __name__ == "__main__":
    app = Fmd3App()
    app.run()
