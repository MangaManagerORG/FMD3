"""
= This file is used for defining Ttk styles.

All style definitions should live in the function named:

   def setup_ttk_styles()

Use an instance of the ttk.Style class to define styles.

As this is a python module, now you can import any other
module that you need.


== In Pygubu Designer

Pygubu Designer will need to know which style definition file 
you wish to use in your project.

To specify a style definition file in Pygubu Designer:
Go to: Edit -> Preferences -> Ttk Styles -> Browse (button)

Assuming that you have specified a style definition file,
- Use the 'style' combobox drop-down menu in Pygubu Designer
  to select a style that you have defined.
- Changes made to the chosen style definition file will be
  automatically reflected in Pygubu Designer.


The code below shows the minimal example definition file.

"""

import tkinter as tk
import tkinter.ttk as ttk

from customtkinter import ThemeManager, CTkComboBox, CTkFont


def setup_ttk_styles(master=None):



    # return
    ...
    my_font = CTkFont()
    bg_color = ThemeManager.theme["CTkFrame"]["fg_color"]
    text_color = ThemeManager.theme["CTkLabel"]["text_color"]
    selected_color = ThemeManager.theme["CTkButton"]["fg_color"]

    ThemeManager.load_theme("dark-blue")

    style = ttk.Style()
    style.theme_use("default")
    style.configure("primary.TButton",
                    font=my_font,
                    background="#4582EC",
                    foreground="white")
    style.configure("secondary.TButton",
                    font=my_font,
                    background="#ADB5BD",
                    foreground="white")
    style.configure("warning.TButton",
                    font=my_font,
                    background="#F0AD4E",
                    foreground="white")
    style.configure("danger.TButton",
                    font=my_font,
                    background="#D9534F",
                    foreground="white")
    style.configure("Treeview",
                    background="#2a2d2e",
                    foreground="white",
                    rowheight=25,
                    fieldbackground="#343638",
                    bordercolor="#343638",
                    borderwidth=0)


    style.configure("Treeview.Heading",
                    background="#565b5e",
                    foreground="white",
                    relief="flat")
    style.map("Treeview.Heading",
              background=[('active', '#3484F0')])

    # style.map('Treeview', background=[('selected', bg_color)], foreground=[('selected', selected_color)])
    style.map('Treeview', background=[('selected', '#22559b')])


    #
    #

    # {'corner_radius': 6, 'border_width': 2, 'fg_color': ['#F9F9FA', '#343638'], 'border_color': ['#979DA2', '#565B5E'],
    # 'button_color': ['#979DA2', '#565B5E'], 'button_hover_color': ['#6E7174', '#7A848D'], 'text_color': ['gray14', 'gray84'],
    # 'text_color_disabled': ['gray50', 'gray45']}

