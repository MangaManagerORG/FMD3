import json
import logging
from pathlib import Path
from tkinter import TclError
from tkinter.ttk import Treeview

from FMD3.sources.SearchResult import SearchResult
from .baseui import BaseUI
from .taskmanager import TaskManager
from .. import api


sources = api.get_sources()


class App(BaseUI):

    def __init__(self):
        super().__init__()

        self.settings = {}
        self.selected_source_id = None

        """Stores keypair values of libraries"""
        self.settings = json.loads(api.get_settings())
        self.settings_libraries = {}
        self.task_manager = TaskManager()


        """Dictionary storing the series object identified by the series id"""
        self.data_series_search_results: dict[str, SearchResult] = {}

        self.last_search_selected_item = None  # Stores the last selected item to later check and not reload a loaded series on double click

        """Initialization of values"""
        self.widget_series_source_optionmenu.configure(values=[s.NAME for s in sources])

        """Track variables to them callbacks"""
        self.var_series_search_entry.trace_add('write', self.on_series_search_entry_input)


    """
    Settings SaveTo
    """

    def on_settings_saveto_add_library(self):
        # Get variables
        path_var = self.var_settings_saveto_lib_path
        alias_var = self.var_settings_saveto_lib_alias
        path = path_var.get()
        alias = alias_var.get()

        # Update localdict
        self.settings_libraries[alias] = path

        # Fetch and insert lib in treeview
        tree = self.builder.get_object("widget_settings_saveto_lib_treeview")
        tree.insert('', 'end', path, values=(alias, path))

        # Append to settings
        self.settings["Core"].get("libraries_alias_paths_list")["value"].append({"alias": alias, "path": path})

        # Clear entries
        path_var.set("")
        alias_var.set("")


    """
    #########################
    Series Tab implementation
    #########################
    """

    """
    On source selected
    """
    def on_series_source_selected(self,*_):
        selected_value = self.var_series_selected_source_name.get()
        source = list(filter(lambda s: s.NAME == selected_value, sources))
        if not source:
            self.selected_source_id = None
        else:
            self.selected_source_id = source[0].ID
            # selected_value = values[selected_index][1]  # Extract the second element of the tuple

    """
    Series search implementation
    """

    def on_series_search_entry_input(self, *_):
        value = self.var_series_search_entry.get()
        if not value or len(value) <= 2:
            return

        ext = self.selected_source_id
        if not ext:
            return
        source_id = self.selected_source_id
        self.task_manager.submit(api.query_series, self.cb__fetch_series_by_name, source_id, value)

    def cb__fetch_series_by_name(self, future):
        self.proc_update_search_list(future.result())

    def proc_update_search_list(self, series_list:list[SearchResult]):
        self.widget_series_search_treeview.delete(*self.widget_series_search_treeview.get_children())
        self.search_delay = False
        logging.debug("updating search list")
        tree = self.widget_series_search_treeview
        for series in series_list:
            self.data_series_search_results[series.series_id] = series
            tree.insert('', 'end', series.series_id, text=series.title)
        self.is_delayed_search = False

    """
    Series search on item selection implementation
    """

    def on_series_search_item_selected(self, event):
        # widget_series_search_treeview:Treeview = self.widget_series_search_treeview
        # widget_series_search_treeview.selection_get()


        selected_series_id = event.widget.selection()[0]
        selected_series = self.data_series_search_results[selected_series_id]

        series_id = selected_series.series_id
        if self.last_search_selected_item:
            if series_id == self.last_search_selected_item:
                return
        self.last_search_selected_item = series_id
        self.task_manager.submit(api.get_series_info, self.cb__get_series_info_from_data, self.selected_source_id, series_id)

    def cb__get_series_info_from_data(self, future):
        self.mainwindow.after(0, self.proc_get_series_info_from_data, future.result())

    def proc_get_series_info_from_data(self, data: dict):
        if not data:
            return
        series_id = data["id"]
        self.selected_source_id = data.get("source_id")
        self.selected_series_id = series_id
        self.add_series_detail(data)
        # Clear chapter treeview
        self.widget_series_chapter_treeview.delete(*self.widget_series_chapter_treeview.get_children())
        self.mainwindow.update_idletasks()

        # Get folder name for the selected series
        # Should the series exist and have a save_to, block the saveto inputs
        if data.get("save_to", None) is not None:
            # Disable both inputs as there is already one saved in the db
            self.enable_series_saveto_inputs(False)
            self.var_series_saveto_final_path.set(data.get("save_to"))
        else:
            parent = self.settings["Core"].get("default_download_path", "")["value"]
            website = None
            author = None
            artist = None
            manga = data.get("title")
            sanitized_folder_name = api.get_series_folder_name(website=website, manga=manga, author=author,
                                                               artist=artist)
            final_path = Path(parent, sanitized_folder_name)
            self.enable_series_saveto_inputs(True)
            self.var_series_saveto_final_path.set(str(final_path))

        self.task_manager.submit(self.widget_series_cover.load_website, None, data.get("cover_url"))
        self.task_manager.submit(self.proc_series_chapters_load_queried_chapters, None, series_id, data)

    def proc_series_chapters_load_queried_chapters(self, series_id: str, data: dict):
        """
        Fetchs and inserts chapters. Diferentiates between downloaded chapters and not downloaded. Downloaded chapters will load from db while not downloaded will load from source

        :param series_id:
        :param data:
        :return:
        """
        # Check if there are downloaded chapters for this series
        has_chapters = False
        if dld_chapters := api.get_chapters(series_id):
            has_chapters = True
            self.widget_series_chapter_nochapters_frame.lower()
            last_in_db = max(dld_chapters, key=lambda x: x["number"])
            # Add chapters with "downloaded" tag
            self.list_chapters_treeview(self.widget_series_chapter_treeview, dld_chapters, ("downloaded",))
            # Prepare query to get the rest of chapters
            args = (self.selected_source_id, series_id, last_in_db.get("number"))
        else:
            # Prepare query to get all chapters
            args = (data["source_id"], series_id)

        # Get chapters from source
        chapters = api.get_source_chapters(*args)
        if chapters:
            has_chapters = True
            self.list_chapters_treeview(self.widget_series_chapter_treeview, chapters, ("not_downloaded",))

        # If there are chapters either downloaded or from source, hide 'series has no chapters'
        if has_chapters:
            self.widget_series_chapter_nochapters_frame.lower()
        else:
            # If no chapters show series has no chapters frame on top
            self.widget_series_chapter_nochapters_frame.lift()
