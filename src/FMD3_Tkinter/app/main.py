import json
import logging
from pathlib import Path

from FMD3.extensions.sources.SearchResult import SearchResult
from .utils import get_sanitized_download

from .baseui import BaseUI
from .taskmanager import TaskManager
from .. import api
from . import widgets
from .widgets.custom_tk_variables import KeyPair

widgets.do_not_clear_import = None

sources = api.get_sources()


class App(BaseUI):

    def __init__(self):
        super().__init__()

        self.settings = {}
        """Stores keypair values of libraries"""
        self.settings = json.loads(api.get_settings())
        self.settings_saveto_libraries = {}
        self.init_settings()
        self.task_manager = TaskManager()

        """Dictionary storing the series object identified by the series id"""
        self.data_series_search_results: dict[str, SearchResult] = {}
        self.last_search_selected_item = None  # Stores the last selected item to later check and not reload a loaded series on double click

        """Initialization of values"""

        """Track variables to them callbacks"""
        self.var_series_search_entry.trace_add('write', self.on_series_search_entry_input)
        self.var_series_saveto_seriesfolder.trace_add("write", self.on_series_saveto_seriesfolder_updated)

        self.widget_tasks_treeview.hanging = self.widget_tasks_treeview.insert("", "end", iid="active", text="Active",
                                                                               open=True)
        self.widget_tasks_treeview.hanging = self.widget_tasks_treeview.insert("", "end", iid="hanging", text="Hanging")
        self.fill_hanging_tasks()
        self.refresh_active_tasks()

        """
        Favourites tab initialization
        """
        """Dictionary storing the current series and chapter childs shown in fav treeview"""
        self.fav_tree_loaded_parents = {}
        self.widget_favourites_treeview.tag_bind('lazy', '<<TreeviewOpen>>', self.child_opened_fav_treeview)
        self.widget_favourites_treeview.bind('<Button-1>', self.child_opened_fav_treeview)
        self.widget_favourites_treeview.tag_configure('favourites_child_chapters', background='#B6B7B7')
        self.on_favourites_refresh()
        self._detached_fav_filter = set()

    def fill_hanging_tasks(self):
        tree = self.widget_tasks_treeview
        tasks = api.get_hanging_tasks()
        for task in tasks:
            tree.insert("hanging", "end", iid=task.chapter_id,
                        text=f"Vol.{task.volume} Ch.{task.number} - {task.chapter_id}",
                        values=("Hanging", None, task.path, str(task.downloaded_at), task.series_id))

    # def fill_active_tasks(self):
    #     tree = self.widget_tasks_treeview
    #     tree.insert("", "end", iid="active", text="Active", open=True)
    #
    #     tasks = api.get_active_tasks()
    #     if tasks is None:
    #         return
    #
    #     for task in tasks:
    #         tree.insert("active", "end", iid=task.chapter_id,
    #                     text=f"Vol.{task.volume} Ch.{task.number} - {task.chapter_id}",
    #                     values=("Hanging", None, task.path, str(task.downloaded_at), task.series_id),
    #                     )

    def refresh_active_tasks(self):
        logging.getLogger().info("Refreshing active tasks")
        tree = self.widget_tasks_treeview
        tasks = api.get_active_tasks()
        active_ids = [chapter.chapter_id for chapter, status in tasks]
        delete_ids = [chapter_id for chapter_id in tree.get_children("hanging") if chapter_id in active_ids]
        tree.delete(*delete_ids)
        tree.delete(*tree.get_children("active"))

        for task, task_status in tasks:
            tree.insert("active", "end", iid=task.chapter_id,
                        text=f"Vol.{task.volume} Ch.{task.number} - {task.chapter_id}",
                        values=(task_status, None, task.path, str(task.downloaded_at), task.series_id),
                        )
        self.mainwindow.after(3000, self.refresh_active_tasks)

    """
    #########################
    Series Tab implementation
    #########################
    """

    def pre_series_sources_loaded_sources(self, *_):
        # self.widget_series_source_optionmenu
        sources_list = [KeyPair(s.NAME, s.ID)
                        for s in sources]
        self.widget_series_source_optionmenu.configure(values=sources_list)

    @property
    def selected_source_id(self):
        return self.var_series_selected_source.get().value

    """
    Series search implementation
    """

    def on_series_search_entry_input(self, *_):
        if self.selected_source_id is None:
            return
        if len(value := self.var_series_search_entry.get()) <= 2:
            return
        self.task_manager.submit(api.query_series, self.cb__fetch_series_by_name, self.selected_source_id, value)

    def cb__fetch_series_by_name(self, future):
        self.proc_update_search_list(future.result())

    def proc_update_search_list(self, series_list: list[SearchResult]):
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
        selected_series_id = event.widget.selection()
        if not selected_series_id:
            return
        selected_series = self.data_series_search_results[selected_series_id[0]]

        series_id = selected_series.series_id
        if self.last_search_selected_item:
            if series_id == self.last_search_selected_item:
                return
        self.last_search_selected_item = series_id
        self.task_manager.submit(api.get_series_info, self.cb__get_series_info_from_data, self.selected_source_id,
                                 series_id)

    def cb__get_series_info_from_data(self, future):
        self.mainwindow.after(0, self.proc_get_series_info_from_data, future.result())

    def proc_get_series_info_from_data(self, data: dict):
        if not data:
            return
        series_id = data["id"]
        # todo: fill ource id from data
        # self.var_series_selected_source.set(KeyPair("SavedSource",data.get("source_id")))
        # self.selected_source_id = data.get("source_id")
        # self.selected_series_id = series_id
        self.add_series_detail(data)
        # Clear chapter treeview
        self.widget_series_chapter_treeview.delete(*self.widget_series_chapter_treeview.get_children())
        self.mainwindow.update_idletasks()

        # Get folder name for the selected series
        # Should the series exist and have a save_to, block the saveto inputs
        if data.get("save_to", None) is not None:
            # Disable both inputs as there is already one saved in the db
            self.enable_series_saveto_inputs(False)
            self.var_series_saveto_seriesfolder.set("")
            self.var_series_saveto_final_path.set(data.get("save_to"))
        else:
            parent = self.settings["Core"].get("default_download_path", "")["value"]
            website = None
            author = None
            artist = None
            manga = data.get("title")

            sanitized_folder_name = api.get_series_folder_name(website=website, manga=manga, author=author,
                                                               artist=artist)
            self.var_series_saveto_seriesfolder.set(sanitized_folder_name)
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

    """
    On output library selected
    """

    def pre_series_saveto_library_selected(self, *_):
        """
        Fills the OptionMenu with the current loaded libraries
        :return:
        """
        widget = self.widget_series_saveto_library_optionmenu
        libs = []
        for id_ in self.settings_saveto_libraries:
            libs.append(KeyPair(self.settings_saveto_libraries[id_]["alias"], str(id_)))

        widget.configure(values=libs)

    def on_series_saveto_library_selected(self, *args):
        self.cb__update_series_saveto_final_path()

    def on_series_saveto_seriesfolder_updated(self, *args):
        self.cb__update_series_saveto_final_path()

    def cb__update_series_saveto_final_path(self, *_, data=None):

        if data:
            folder_name = data.get("title")
            self.var_series_saveto_library.set(folder_name)
        else:
            folder_name = self.var_series_saveto_seriesfolder.get()

        # todo fetch def library from settings
        # lib_path = self.settings_libraries.get(self.default_series_downloads_path.get(), '.')
        keypair = self.var_series_saveto_library.get()
        if keypair.is_label() is False:
            lib_path = self.settings_saveto_libraries[int(keypair.value)]["path"]
        else:
            lib_path = "."

        series_path_or_modifie = folder_name

        sanitized_download_lib_path = get_sanitized_download(lib_path, manga=series_path_or_modifie)
        if data:
            if data.get("save_to", None) is not None:
                self.widget_series_saveto_seriesfolder_entry.configure(state="disabled")
                self.widget_series_saveto_library_optionmenu.configure(state="disabled")
                self.var_series_saveto_final_path.set(data.get("save_to"))
                # self.series_destination_path.set(data.get("save_to"))
                return
        self.widget_series_saveto_seriesfolder_entry.configure(state="normal")
        self.widget_series_saveto_library_optionmenu.configure(state="readonly")
        self.var_series_saveto_final_path.set(str(sanitized_download_lib_path.resolve()))

    """
    Download options
    """

    def on_series_chapters_actionmenu_download(self, action):
        ...
        print("sada")
        series_id = self.last_search_selected_item
        source_id = self.selected_source_id
        output_path = self.var_series_saveto_final_path.get()
        match action:
            case "Download Selected":
                chapter_ids = self.widget_series_chapter_treeview.selection()
                api.download_chapters(source_id=source_id, series_id=series_id, chapter_ids=chapter_ids,
                                      output_path=output_path)
            case "Download All":
                api.download_chapters(source_id=source_id, series_id=series_id, chapter_ids="all",
                                      output_path=output_path)

    def on_series_chapters_actionmenu_favourite(self, action):
        series_id = self.last_search_selected_item
        source_id = self.selected_source_id
        output_path = self.var_series_saveto_final_path.get()
        if action == "Add to fav":
            api.add_fav_series(source_id=source_id, series_id=series_id, output_path=output_path)
        elif action == 'Add to fav & add to download queue':
            api.download_chapters(source_id=source_id, series_id=series_id, chapter_ids="all",
                                  output_path=output_path, enable_series=True, fav_series=True)
        self.on_favourites_refresh()

    """
    #########################
    SETTINGS TAB IMPLEMENTATION
    #########################
    """

    """
    CUSTOM LIBRARIES
    """

    def init_settings(self):
        # I'll be saving these settings in the UI category. I don't feel they fit in the core section as all this
        # custom lib thingy is a helper for users to comfortab  ly choose where to download
        if self.settings.get("UI", None) is None:
            self.settings["UI"] = {
                "user_libraries": {
                    "key": "user_libraries",
                    "name": "User defined libraries",
                    "value": None,
                    "values":[],
                    "type": 1,
                    "tooltip": "",
                    "def_value": [],
                }
            }
        items = []

        # Load default download library

        default_lib = self.settings["UI"].get("user_libraries",None)["value"]
        id_ = id(default_lib)
        self.settings_saveto_libraries[id_] = {"alias": default_lib["alias"], "path": default_lib["path"]}
        self.widget_settings_saveto_libraries_treeview.insert('', 'end', id_,
                                                              values=(default_lib["alias"], default_lib["path"]))
        def_keypair = KeyPair(self.settings_saveto_libraries[id_]["alias"], str(id_))
        self.var_settings_saveto_lib_default.set(def_keypair)

        # fill def download library comboboxes
        self.widget_settings_saveto_libraries_default_optionmenu.set(def_keypair)
        self.widget_series_saveto_library_optionmenu.set(def_keypair)
        self.on_series_saveto_library_selected()

        # Load the rest of user-defined libraries

        for library in self.settings["UI"].get("user_libraries",None)["values"]:
            if library == default_lib:
                continue
            id_ = id(library)
            self.settings_saveto_libraries[id_] = {"alias": library["alias"], "path": library["path"]}
            # items.append(KeyPair(library["alias"], id_))
            self.widget_settings_saveto_libraries_treeview.insert('', 'end', id_,
                                                                  values=(library["alias"], library["path"]))

    """
    Settings SaveTo
    """

    def on_settings_saveto_libraries_add_library(self, *_):
        # Get variables
        path_var = self.var_settings_saveto_lib_path
        alias_var = self.var_settings_saveto_lib_alias

        path = path_var.get()
        alias = alias_var.get()
        if path is None or alias is None:
            return
        lib = {"alias": alias, "path": path}

        filter_alias = [id_ for id_ in self.settings_saveto_libraries if
                        alias == self.settings_saveto_libraries[id_]["alias"]]

        tree = self.builder.get_object("widget_settings_saveto_libraries_treeview")

        if filter_alias:
            id_ = filter_alias[0]
            tree.item(str(id_), values=(alias, path))
        else:
            id_ = id(lib)
            tree.insert('', 'end', str(id_), values=(alias, path))
        # Append to loaded lib
        self.settings_saveto_libraries[id_] = lib
        # Fetch and insert lib in treeview

        # Append to settings
        self.settings["UI"]["user_libraries"]["values"].append({"alias": alias, "path": path})

        # Clear entries
        path_var.set("")
        alias_var.set("")

    def settings_saveto_libraries_default_optionmenu(self, keypair):
        """
        Called when the user changes default download library. Updates def download path in settings
        :param _:
        :return:
        """
        keypair_ = self.settings_saveto_libraries[int(keypair.value)]
        self.settings["UI"]["user_libraries"]["value"] = {"alias": keypair_["alias"], "path": keypair_["path"]}
        self.settings["Core"]["default_download_path"]["value"] = keypair_["path"]

        # TODO: Add call to update settings

    def pre_settings_saveto_libraries_default_optionmenu(self, *_):
        """
        Fills the optionmenu widget with values from user libraries
        :return:
        """
        widget = self.widget_settings_saveto_libraries_default_optionmenu
        libs = []
        for id_ in self.settings_saveto_libraries:
            libs.append(KeyPair(self.settings_saveto_libraries[id_]["alias"], str(id_)))

        widget.configure(values=libs)

    """
    Save settings
    """

    def on_settings_save_pressed(self, *_):
        api.update_settings(json.dumps(self.settings))

    """
    #########################
    FAVOURITES TAB IMPLEMENTATION
    #########################
    """

    def on_favourites_refresh(self, *_):
        tree = self.widget_favourites_treeview
        self.fav_tree_loaded_parents = {}
        tree.delete(*tree.get_children())
        series_list = api.get_fav_series(sort="dateadded", order="desc")

        for series in series_list:
            if series.get("series_id") not in self.fav_tree_loaded_parents:
                source = api.get_source(source_id=series.get("source_id"))
                if source:
                    source_name = source.get("name")
                else:
                    source_name = "Unknown(Not Loaded)"
                item_id = self.widget_favourites_treeview.insert('', 'end', series.get("series_id"),
                                                                 text=series.get("title"),
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
        # self.fav_sort_date_added()
