#!/usr/bin/python3
import pathlib
import tkinter as tk
from tkinter import ttk
import customtkinter
import pygubu

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
        selected_color = self.mainwindow._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkButton"]["fg_color"])

        treestyle = ttk.Style()
        treestyle.theme_use('default')
        treestyle.configure("Treeview", background=bg_color, foreground=text_color, fieldbackground=bg_color,
                            borderwidth=0)
        treestyle.map('Treeview', background=[('selected', bg_color)], foreground=[('selected', selected_color)])
        self.mainwindow.bind("<<TreeviewSelect>>", lambda event: self.mainwindow.focus_set())


        tree: ttk.Treeview = self.builder.get_object("test_checkbox_tree")
        tree.insert("", "end", values=("Vol.2", "Ch.45", "Title of the chapter"))
        tree.insert("", "end", values=("Vol.2", "Ch.46", "Title of the chapter"))
        tree.insert("", "end", values=("Vol.2", "Ch.47", "Title of the chapter"))
        tree.insert("", "end", values=("Vol.2", "Ch.48", "Title of the chapter"))


    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = Fmd3App()



    app.run()


