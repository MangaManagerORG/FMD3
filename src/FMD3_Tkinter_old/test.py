#!/usr/bin/python3
import pathlib
import tkinter as tk
from tkinter import ttk
import customtkinter
import pygubu
import ttkwidgets

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "FMD3.ui"
import styles
import widgets

class Fmd3App:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder(on_first_object=styles.setup_ttk_styles)
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: customtkinter.CTk = builder.get_object("ctk1", master)
        builder.connect_callbacks(self)
        ###Treeview Customisation (theme colors are selected)

        # style = ttk.Style()
        # style.theme_use('default')

        tree: ttk.Treeview = self.builder.get_object("series_chapterlist_treeview")
        tree.insert("", "end", values=("Vol.2", "Ch.45", "Title of the chapter"))
        tree.insert("", "end", values=("Vol.2", "Ch.46", "Title of the chapter"))
        tree.insert("", "end", values=("Vol.2", "Ch.47", "Title of the chapter"))
        tree.insert("", "end", values=("Vol.2", "Ch.48", "Title of the chapter"))

        tree: ttk.Treeview = self.builder.get_object("installed_sources_treeview")
        tree.insert("", "end", values=("Alias", "Path"))
        tree.insert("", "end", values=("Alias", "Path"))
        tree.insert("", "end", values=("Alias", "Path"))
        tree.insert("", "end", values=("Alias", "Path"))

        tree = self.builder.get_object("series_result")
        tree.delete(*tree.get_children())
        tree.insert('', 'end', "a", text="a title")
        tree.insert('', 'end', "B", text="a title")
        tree.insert('', 'end', "C", text="a title")
        tree.insert('', 'end', "D", text="a title")


        self.mainwindow.bind("<<TreeviewSelect>>", lambda event: self.mainwindow.focus_set())



    def change_appearance_mode_event(self, current_value):
        customtkinter.set_appearance_mode(current_value)

    def change_scaling_event(self, current_value):
        new_scaling_float = int(current_value.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = Fmd3App()

    app.run()
