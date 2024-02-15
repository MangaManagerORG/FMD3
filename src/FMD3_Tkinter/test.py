#!/usr/bin/python3
import pathlib
import tkinter as tk
from tkinter import ttk
import customtkinter
import pygubu
import ttkwidgets

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "FMD3.ui"


class Fmd3App:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: customtkinter.CTk = builder.get_object("ctk1", master)
        builder.connect_callbacks(self)
        ###Treeview Customisation (theme colors are selected)
        bg_color = self.mainwindow._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"])
        text_color = self.mainwindow._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkLabel"]["text_color"])
        selected_color = self.mainwindow._apply_appearance_mode(
            customtkinter.ThemeManager.theme["CTkButton"]["fg_color"])
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])

        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="flat")
        style.map("Treeview.Heading",
                  background=[('active', '#3484F0')])

        style.map('Treeview', background=[('selected', bg_color)], foreground=[('selected', selected_color)])

        style.configure("ToggledFrame", )

        self.mainwindow.bind("<<TreeviewSelect>>", lambda event: self.mainwindow.focus_set())

        tree: ttk.Treeview = self.builder.get_object("selected_series_chapter_treeview")
        tree.insert("", "end", values=("Vol.2", "Ch.45", "Title of the chapter"))
        tree.insert("", "end", values=("Vol.2", "Ch.46", "Title of the chapter"))
        tree.insert("", "end", values=("Vol.2", "Ch.47", "Title of the chapter"))
        tree.insert("", "end", values=("Vol.2", "Ch.48", "Title of the chapter"))

        tree: ttk.Treeview = self.builder.get_object("installed_sources_treeview")
        tree.insert("", "end", values=("Alias", "Path"))
        tree.insert("", "end", values=("Alias", "Path"))
        tree.insert("", "end", values=("Alias", "Path"))
        tree.insert("", "end", values=("Alias", "Path"))




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
