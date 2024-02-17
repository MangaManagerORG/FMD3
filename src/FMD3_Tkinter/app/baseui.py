#!/usr/bin/python3
import json
import pathlib
import tkinter as tk
from abc import abstractmethod

import pygubu
import customtkinter
from FMD3_Tkinter import styles
from FMD3_Tkinter import api

PROJECT_PATH = pathlib.Path(__file__).parent.parent
PROJECT_UI = PROJECT_PATH / "FMD3.ui"


class BaseUi:
    def __init__(self, master=None, translator=None):

        # Code init vars
        self.settings = json.loads(api.get_settings())
        self.settings_libraries = {}

        # Pygubu init
        self.builder = builder = pygubu.Builder(
            translator=translator,
            on_first_object=styles.setup_ttk_styles)

        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: customtkinter.CTk = builder.get_object("ctk1", master)

        self.selected_source_name: tk.StringVar = None
        self.query_stringvar: tk.StringVar = None
        self.series_browser_url_entry_var: tk.StringVar = None
        self.default_series_downloads_path: tk.StringVar = None
        self.series_destination_path: tk.StringVar = None
        self.series_final_download_dest: tk.StringVar = None
        self.settings_lib_alias_entry: tk.StringVar = None
        self.settings_lib_path_entry: tk.StringVar = None
        self.default_downloads_path: tk.StringVar = None
        self.appearance_var: tk.StringVar = None
        self.scaling_var: tk.StringVar = None

        builder.import_variables(self)





    @staticmethod
    def change_appearance_mode_event(new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    @staticmethod
    def change_scaling_event(new_scaling):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    @abstractmethod
    def series_tab_search_by_url(self):
        pass

    @abstractmethod
    def settings_load_libs_from_treeview(self, current_value):
        pass

    @abstractmethod
    def add_library_to_treeview(self):
        pass



    @abstractmethod
    def fav_sort_date_added(self):
        pass

    @abstractmethod
    def child_opened_fav_treeview(self, event=None):
        pass
