#!/usr/bin/python3
import logging
import pathlib
import tkinter
import tkinter as tk
from tkinter import END
from tkinter.ttk import Treeview

import pygubu

import customtkinter

from FMD3.api.models.chapters import ChapterResponse
from .widgets.custom_tk_variables import KeyPairVar, KeyPair
from .styles import setup_ttk_styles
from . import widgets
from .. import api

PROJECT_PATH = pathlib.Path(__file__).parent.parent
PROJECT_UI = PROJECT_PATH / "FMD3.ui"



class BaseUI:
    def __init__(self, master=None, translator=None):
        self.builder = builder = pygubu.Builder(translator,on_first_object=setup_ttk_styles)
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: customtkinter.CTk = builder.get_object("ctk1", master)

        # builder.connect_callbacks(self)

        """
        Widgets definitions
        """
        self.widget_series_source_optionmenu = self.builder.get_object("widget_series_source_optionmenu")
        self.widget_series_search_treeview = self.builder.get_object("widget_series_search_treeview")
        self.widget_series_cover = self.builder.get_object("widget_series_cover")
        self.widget_series_chapter_treeview = self.builder.get_object("widget_series_chapter_treeview")
        self.widget_series_chapter_nochapters_frame = self.builder.get_object("widget_series_chapter_nochapters_frame")
        self.widget_series_saveto_library_optionmenu = self.builder.get_object("widget_series_saveto_library_optionmenu")
        self.widget_series_saveto_seriesfolder_entry = self.builder.get_object("widget_series_saveto_seriesfolder_entry")
        # Settings
        self.widget_settings_saveto_libraries_treeview = self.builder.get_object("widget_settings_saveto_libraries_treeview")

        self.widget_settings_saveto_libraries_default_optionmenu = self.builder.get_object("widget_settings_saveto_libraries_default_optionmenu")

        # Tasks
        self.widget_tasks_treeview:Treeview = self.builder.get_object("widget_tasks_treeview")

        # Favourites
        self.widget_favourites_treeview:Treeview  = self.builder.get_object("widget_favourites_treeview")

        """
        Custom variable definition and track to widget
        """
        self.var_series_selected_source = KeyPairVar(name="series_selected_source", value=KeyPair("Select Source",None,True))
        self.widget_series_source_optionmenu.configure(variable=self.var_series_selected_source)

        self.var_series_saveto_library = KeyPairVar(name="series_saveto_library", value=KeyPair("No library selected",None,True))
        self.widget_series_saveto_library_optionmenu.configure(variable=self.var_series_saveto_library)

        self.var_settings_saveto_lib_default = KeyPairVar(name="var_settings_saveto_lib_default", value=KeyPair("Select default download library",True))
        self.widget_settings_saveto_libraries_default_optionmenu.configure(variable=self.var_settings_saveto_lib_default)
        """
        Variable definitions
        """

        #Static variables
        self.var_series_chapter_selection_action_menu = tk.StringVar(name="series_chapter_selection_action", value=None)
        self.var_series_chapter_download_action_menu = tk.StringVar(name="series_chapter_download_action", value=None)
        self.var_series_chapter_favourites_action_menu = tk.StringVar(name="series_chapter_favourites_action", value=None)

        # Variables used in settings_saveto
        self.var_settings_saveto_lib_alias = tk.StringVar(name="var_settings_saveto_lib_alias", value=None)
        self.var_settings_saveto_lib_path = tk.StringVar(name="var_settings_saveto_lib_path", value=None)
        self.var_settings_saveto_lib_default = tk.Variable(name="var_settings_saveto_lib_default", value=None)
        self.var_settings_saveto_mangafolder_name = tk.StringVar(name="var_settings_saveto_mangafolder_name", value=None)
        self.var_settings_saveto_chapter_name = tk.StringVar(name="var_settings_saveto_chapter_name", value=None)
        self.var_settings_saveto_dogenerate_manga_folder = tk.Variable()
        # Variables used for series search
        self.var_series_search_entry = tk.StringVar(name="var_series_search_entry",value=None)

        # Variables used in series_saveto
        self.var_series_saveto_final_path = tk.StringVar(name="var_series_saveto_final_path", value=None)
        self.var_series_saveto_seriesfolder = tk.StringVar(name="var_series_saveto_seriesfolder", value=None)

        builder.connect_callbacks(self)
        builder.import_variables(self)
        # Variable used to store selected source

        self.var_series_chapter_selection_action_menu.set("Select")
        self.var_series_chapter_download_action_menu.set("Download")
        self.var_series_chapter_favourites_action_menu.set("Favourite")

    @staticmethod
    def change_appearance_mode_event(new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    @staticmethod
    def change_scaling_event(new_scaling):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def run(self):
        self.mainwindow.mainloop()

    def add_series_detail(self, data: dict):
        """
        Unlocks the :class:`customtkinter.CTkTextbox` and fills it with the data from the series
        :param series_detail_widget: :class:`customtkinter.CTkTextbox`
        :param data: dict containing: ["title","authors","artists","generes,"status","description"]
        :return:
        """
        series_detail_widget = self.builder.get_object("widget_series_details_textbox")
        series_detail_widget.configure(state=tkinter.NORMAL)
        series_detail_widget.delete('1.0', END)

        add_detail_entry(series_detail_widget, data, "Title", "title", tag="")
        add_detail_entry_array(series_detail_widget, data, "Author(s)", "authors", tag="")
        add_detail_entry_array(series_detail_widget, data, "Artist(s)", "artists", tag="")
        add_detail_entry_array(series_detail_widget, data, "Genre(s)", "genres", tag="")
        add_detail_entry(series_detail_widget, data, "Status", "status", tag="")
        add_detail_entry(series_detail_widget, data, "Summary", "description", tag="")
        series_detail_widget.configure(state="disabled")

    def enable_series_saveto_inputs(self, value: bool):
        self.builder.get_object("widget_series_saveto_library_optionmenu").configure(
            state="normal" if value else "disabled")
        self.builder.get_object("widget_series_saveto_seriesfolder_entry").configure(
            state="normal" if value else "disabled")

    @staticmethod
    def list_chapters_treeview(widget, chapter_list: list[ChapterResponse], tags: tuple[str]):
        for chapter in chapter_list:
            try:
                widget.insert('', 'end', chapter.chapter_id,
                              values=(chapter.volume, chapter.number, chapter.title), tags=tags)
            except Exception as e:
                logging.getLogger().error(f"Unhandled exception inserting one chapter: '{e} - {chapter.number}  {chapter.title}'")

    def on_series_chapters_actionmenu(self, menu, value):
        match menu:
            case "Select":
                self.on_series_chapters_actionmenu_select(value)
            case "Download":
                self.on_series_chapters_actionmenu_download(value)
            case "Favourite":
                self.on_series_chapters_actionmenu_favourite(value)

    def on_series_chapters_actionmenu_select(self, value):
        tree = self.widget_series_chapter_treeview
        if value == "None":
            tree.uncheck_all()
        if value == "All":
            tree.check_all()






        # if value == "All":
        #     return
        #
        # if value == "Selected":
        #     self.builder.get_object("series_output_save_to_entry").configure(state="readonly")
        #     chapters_treeview = self.builder.get_object("series_chapterlist_treeview")
        #     to_download_ids = chapters_treeview.selection()
        #     to_download_series = self.selected_series_id
        #     self.builder.get_object("series_output_save_to_entry").configure(state="disabled")
        #     self.builder.get_object("settings_def_series_lib_combo").configure(state="disabled")
        #     api.download_chapters(self.selected_source_id, to_download_series, to_download_ids,
        #                           output_path=self.builder.get_variable(
        #                               "series_final_download_dest").get())  # Todo save to

    def on_series_chapters_actionmenu_favourite(self, action):
        ...

    def filter_favourites_treeview(self):
        tree = self.widget_series_chapter_treeview
        # Get the filter text from the entry widget
        filter_text = self.builder.get_object("favourites_tab_filter_entry").get().lower()

        # Clear existing items in the tree
        children = list(self._detached_fav_filter) + list(tree.get_children())
        self._detached_fav_filter = set()

        i_r = -1
        for item_id in children:
            text = tree.item(item_id)[
                'text'].lower()  # already contains the strin-concatenation (over columns) of the row's values
            if filter_text in text:
                i_r += 1
                tree.reattach(item_id, '', i_r)
            else:
                self._detached_fav_filter.add(item_id)
                tree.detach(item_id)

    def child_opened_fav_treeview(self, *_):
        tree = self.widget_favourites_treeview
        series_id = tree.focus()
        if not series_id:
            return
        # Check if the item has been loaded
        if not self.fav_tree_loaded_parents.get(series_id, False):
            # Load the children of the parent item
            self.load_children(series_id, )
            # Mark the parent as loaded
            self.fav_tree_loaded_parents[series_id] = True
    def load_children(self, parent_id):
        # Simulate loading children from a data source
        for chapter in sorted(api.get_chapters(parent_id), key=lambda x: x.get("number")):
            child_id = self.widget_favourites_treeview.insert(parent_id, 'end', text=chapter.get("title") or "",
                                                       values=(
                                                           f'Ch.{chapter["number"]} Vol.{chapter["volume"]}', "",
                                                           chapter.get("path"),
                                                           chapter.get("download_date"),
                                                           chapter.get("status"), "", "", ""),
                                                       tags=("favourites_child_chapters",))
"""Helper functions"""


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

