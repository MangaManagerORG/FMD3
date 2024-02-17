# import json
# import pathlib
# import tkinter as tk
# from pathlib import Path
# from tkinter import ttk
# from tkinter.tix import CheckList
# import pygubu
# import sv_ttk
# from FMD3_Tkinter.i18n import translator
#
# from FMD3_Tkinter import api
# from FMD3_Tkinter.__version__ import __version__
# from FMD3_Tkinter.client_settings import Settings as ClientSettings
# from .favorites import Favourites
# from .series import Series
# from .settings import Settings
# from .widgets.TtkCheckList import TtkCheckList
#
#
# class App(Favourites, Series, Settings):
#     # Settings stuff
#     settings_libraries: dict
#
#     def __init__(self):
#         Settings.__init__(self)
#         Favourites.__init__(self)
#         Series.__init__(self)
#         self.builder.get_object("app_info_label").config(text=f"Running: FMD3 Client v{__version__} | API {api.api_version()}")
#
#     def add_library_to_treeview(self, *_):
#         alias = self.builder.get_variable("settings_lib_alias_entry").get()
#         path = self.builder.get_variable("settings_lib_path_entry").get()
#
#         self.settings_libraries[alias] = path
#
#         tree = self.builder.get_object("settings_libraries_treeview")
#
#         tree.insert('', 'end', path, values=(alias, path))
#         self.settings["Core"].get("libraries_alias_paths_list")["value"].append({"alias": alias, "path": path})
#         print("sads")
#
#     def settings_load_libs_from_treeview(self):
#         libs = self.settings_libraries
#         tree = self.builder.get_object("settings_libraries_treeview")
#
#         lib_selector_combo = self.builder.get_object("settings_def_lib_combo")
#         series_lib_selector_combo = self.builder.get_object("settings_def_series_lib_combo")
#
#         lib_selector_combo['values'] = list(libs)
#         series_lib_selector_combo['values'] = list(libs)
#
#     def settings_load_save_to_treeview_from_settings(self):
#         tree = self.builder.get_object("settings_libraries_treeview")
#         for lib in self.settings["Core"].get("libraries_alias_paths_list")["value"]:
#             # libs.append(lib["alias"] + " - " + lib["path"])
#             self.settings_libraries[lib["alias"]] = lib["path"]
#             tree.insert('', 'end', lib["path"], values=(lib["alias"], lib["path"]))
#
#     def series_update_final_dest(self, *_):
#         default_series_downloads_path = self.builder.get_variable("default_series_downloads_path")
#         series_destination_path = self.builder.get_variable("series_destination_path")
#         default_lib_path = self.builder.get_variable("default_downloads_path")
#         series_final_download_dest = self.builder.get_variable("series_final_download_dest")
#         series_final_download_dest.set(Path(self.settings_libraries.get(default_series_downloads_path.get(),
#                                                                         self.settings_libraries.get("default_lib_path",
#                                                                                                     "")),
#                                             series_destination_path.get()))
#
#     def nb_tab_changed(self, event):
#         match event.widget.tab(event.widget.select(), "text"):
#             # case "Favorites":
#             #     self.load_favourites(get_series("dateadded", "desc", 10))
#             case _:
#                 ...
#
#
# PROJECT_PATH = pathlib.Path(__file__).parent.parent
# PROJECT_UI = PROJECT_PATH / "ui_test.ui"
# api.check_source_updates()
# sources = api.get_sources()
#
# def update_sources():
#     sources = api.get_sources()
#
#
# available_sources = {}
# installed_sources = set
#
#
# class TkinterUI(App):
#     def test(self, *args):
#         print("asdas")
#
#     def do_popup(self, event):
#         m = self.builder.get_object("fav_treeview_ctx_menu")
#
#         try:
#             selected_item = self.favourites_treeview.identify_row(event.y)
#             if selected_item in self.fav_tree_loaded_parents:
#                 self.favourites_treeview.selection_set(selected_item)
#                 # m.selection = self.favourites_treeview.set(self.favourites_treeview.identify_row(event.y))
#                 # m.post(event.x_root, event.y_root)
#                 m.tk_popup(event.x_root, event.y_root)
#         finally:
#             m.grab_release()
#
#     def show_edit_save_to(self, *args):
#         # "series_destination_path_edit"
#         # "top_level_edit_save_to"
#         self.builder.get_object('dialog1', self.mainwindow).run()
#         self.builder.connect_callbacks(self)
#         series_id = self.favourites_treeview.selection()
#         vals = self.favourites_treeview.item(series_id, "values")
#
#         toplevel_entry_val = self.builder.get_variable("series_destination_path_edit")
#         toplevel_entry_val.set(vals[2])
#         # top_level.deiconify()
#
#     def update_series_destination_path_submit(self, *args):
#         series_id = self.favourites_treeview.selection()[0]
#         vals = list(self.favourites_treeview.item(series_id, "values"))
#
#         toplevel_entry_val = self.builder.get_variable("series_destination_path_edit")
#         vals[2] = toplevel_entry_val.get()
#         self.favourites_treeview.item(series_id, values=vals)
#         api.update_settings_save_to(series_id, toplevel_entry_val.get())
#         print("edited")
#
#         self.close_series_destination_path_submit()
#
#     def close_series_destination_path_submit(self, *args):
#         top_level = self.builder.get_object('dialog1')
#         toplevel_entry_val = self.builder.get_variable("series_destination_path_edit")
#         toplevel_entry_val.set(None)
#         top_level.close()
#
#     def track_client_setting(self, key):
#         var = self.builder.get_variable(key)
#         # Set the StringVar's value to the initial value of the corresponding attribute
#         val = var.get()
#         if val is not None:
#             var.set(val)
#         # Set up the trace on the StringVar to call a callback when it changes
#         var.trace_add("write", lambda *args: self.update_client_settings(key, var))
#
#     def update_client_settings(self,key,var):
#         ClientSettings().set(key, var.get())
#
#     def apply_settings(self):
#         super().apply_settings()
#
#         ClientSettings().save()
#
#     def __init__(self, master=None):
#
#         self.settings = json.loads(api.get_settings())
#
#         self.builder = builder = pygubu.Builder(translator)
#         builder.add_resource_path(PROJECT_PATH)
#         builder.add_from_file(PROJECT_UI)
#         # Main widget
#         self.mainwindow: tk.Tk = builder.get_object("tk1", master)
#
#         if api._type == "local":
#             self.builder.get_object("settings_client_host_entry").configure(state=tk.DISABLED)
#         else:
#             stw = self.builder.get_variable("settings_client_host_var")
#             val = ClientSettings().get("settings_client_host_var")
#             if val is not None:
#                 stw.set(val)
#             self.builder.get_object("settings_client_host_entry").configure(state=tk.NORMAL)
#         if ClientSettings().get("is_dark_mode_enabled"):
#             sv_ttk.set_theme("dark")
#         self.favourites_treeview = self.builder.get_object("favourites_treeview")
#         self.favourites_treeview.bind("<Button-3>", self.do_popup)
#         self.favourites_treeview: ttk.Treeview
#         self.favourites_treeview.focus()
#
#         self.builder.get_object("fav_treeview_ctx_menu", master)
#         # self.builder.get_object("command2")
#
#         # top2 = tk.Toplevel(self.mainwindow)
#
#         builder.connect_callbacks(self)
#         builder.get_object("source_selector_combobox").config(values=[s["name"] for s in sources])
#
#         self.selected_source_id = None
#         self.search_results = {}
#         self.is_delayed_search = False
#         self.builder.get_object("series_detail").tag_configure("bold", font="Helvetica 12 bold")
#         chapters_treeview = self.builder.get_object("selected_series_chapter_treeview")
#         chapters_treeview.tag_configure('downloaded', background='lime')
#         chapters_treeview.tag_configure('not_downloaded', background='grey')
#         self.series_detail_cover_image = None
#         self.mainwindow.state('zoomed')
#
#         self.track_setting("default_downloads_path")
#         # self.track_checkbox("replace_unicode_char_checkbox","replace_unicode_char_with_entry")
#         self.track_setting("replace_unicode", "replace_unicode_char_with_entry")
#         self.track_setting("replace_unicode_with")
#
#         self.track_setting("generate_series_folder", "manga_folder_name_entry")
#         self.track_setting("series_folder_name")
#
#         # self.track_setting("remove_manga_name_from_chapter_name")
#         self.track_setting("chapter_name")
#
#         self.track_setting("rename_chapter_digits_volume", "rename_volume_digits_spinbox")
#         self.track_setting("rename_chapter_digits_chapter", "rename_chapter_digits_spinbox")
#         self.track_setting("rename_chapter_digits_volume_value")
#         self.track_setting("rename_chapter_digits_chapter_value")
#
#         self.settings_libraries = {}
#         self.track_setting("default_downloads_path")  # ,"settings_def_lib_combo")
#
#         self.track_client_setting("settings_client_host_var")
#         self.track_client_setting("is_dark_mode_enabled")
#
#
#         # Library selection field
#         default_series_downloads_path = builder.get_variable("default_series_downloads_path")
#         default_series_downloads_path.trace_add("write", self.series_update_final_dest)
#
#         # Series field
#         series_destination_path = builder.get_variable("series_destination_path")
#         series_destination_path.trace_add("write", self.series_update_final_dest)
#         super().__init__()
#         self.settings_load_save_to_treeview_from_settings()
#         # cover_frame = self.builder.get_object("frame_test_image")
#         # self.cover_web_frame = HtmlFrame(cover_frame,vertical_scrollbar=False)  # create HTML browser
#         # self.cover_web_frame.pack(side=tk.TOP, fill=tk.BOTH,expand=True)
#
#         # Library selection field set default
#         default_series_downloads_path.set(self.settings["Core"].get("default_downloads_path", None)["value"])
#         self.populate_sources()
#
#     def on_source_selected(self, *_):
#
#         combo = self.builder.get_object("source_selector_combobox")
#         selected_index = combo.current()
#         source = sources[selected_index]
#         self.selected_source_id = source.get("id")
#         # selected_value = values[selected_index][1]  # Extract the second element of the tuple
#
#     # Cross tabs methods
#     def show_selected_in_series_tab(self, *_):
#         tree = self.builder.get_object("favourites_treeview")
#
#         if tree.selection():
#             series_id = tree.selection()[0]
#             values = tree.item(series_id, "values")
#             if not self.selected_source_id:
#                 self.selected_source_id = values[7]
#             data = api.get_series_info(values[7], tree.selection()[0])
#             if data:
#                 self.selected_series_id = series_id
#                 series_result_tree = self.builder.get_object("series_result")
#                 series_result_tree.delete(*series_result_tree.get_children())
#                 self.load_queried_data(series_id, data)
#                 self.builder.get_object("notebook_widget").select(0) # select series tab
#
#     # def populate_sources(self, *_):
#     #     frame = self.builder.get_object("enabled_sources")
#     #     self.cl = TtkCheckList(frame)
#     #     self.cl.add_item("installed", "Installed")
#     #     self.cl.add_item("NotInstalled", "Not Installed")
#     #
#     #     for source in sources:
#     #         self.cl.add_item("installed."+source["id"], source.get("name"),"Installed", True)
#     #         installed_sources.append(source["id"])
#     #     available_sources = api.get_available_sources()
#     #     if available_sources:
#     #         for source in available_sources:
#     #             if source not in installed_sources:
#     #                 self.cl.add_item("not_installed." + source.get("id"), source.get("name"), "NotInstalled")
#     #
#     #     self.cl.pack(anchor="w",fill="both", expand=True)
#     #     # self.cl = CheckList(frame, browsecmd=self.selectItem)
#     #
#     # def selectItem(self, item):
#     #     print(item, self.cl.getstatus(item))
#     def populate_sources(self, *_):
#         parent_frame = self.builder.get_object("enabled_sources")
#         global available_sources, installed_sources
#         available_sources = api.get_available_sources()
#         installed_sources = set()
#
#         self.populate_installed()
#         self.populate_not_installed()
#
#     def populate_not_installed(self):
#         not_installed_frame = self.builder.get_object("settings_sources_not_installed")
#         if available_sources:
#             i =1
#             for source in available_sources:
#                 if source not in installed_sources:
#                     source_obj = available_sources[source]
#
#                     ttk.Label(not_installed_frame, text=source_obj.get("name")).grid(row=i, column=0,
#                                                                                                 sticky="nswe")
#                     ttk.Label(not_installed_frame, text=source_obj.get("version")).grid(row=i, column=1,
#                                                                                                    sticky="nswe")
#                     ttk.Label(not_installed_frame, text=source_obj.get("_has_updates" or False)).grid(row=i, column=2,
#                                                                                                            sticky="nswe")
#                     actions = ttk.Frame(not_installed_frame)
#                     actions.grid(row=i, column=4, sticky="e")
#                     button = ttk.Button(actions, text="Install")
#                     button.configure(command = lambda x=source, btn=button: self.install_source(x,btn))
#                     button.pack(side="right")
#
#
#                     i += 1
#
#     def settings_sources_listing_refresh_btn_call(self):
#         global available_sources, installed_sources
#         api.check_source_updates()
#         available_sources = api.get_available_sources()
#         installed_sources = set()
#         self.update_installed_listing()
#         self.update_not_installed_listing()
#
#     def populate_installed(self):
#         installed_frame = self.builder.get_object("settings_sources_installed")
#         for i, source in enumerate(sources, start=1):
#             # frame = ttk.Frame(installed_frame, width="200")
#             background = "orange" if source.get("has_updates") else None
#             ttk.Label(installed_frame, text=source.get("name"), background=background).grid(row=i, column=0, sticky="nswe")
#             ttk.Label(installed_frame, text=source.get("version"), background=background).grid(row=i, column=1, sticky="nswe")
#             ttk.Label(installed_frame, text=source.get("has_updates") or "False", background=background).grid(row=i, column=2, sticky="nswe")
#
#             actions = ttk.Frame(installed_frame)
#             actions.grid(row=i, column=4, sticky="e")
#             button = ttk.Button(actions, text="Uninstall")
#             button.configure(command=lambda x=source.get("id"),btn=button: self.pre_delete_source(x,button))
#             button.pack(side="right")
#             # if source.get("_has_updates"):
#             button = ttk.Button(actions, text="Update", state="normal" if source.get("has_updates") else "disabled")
#             button.configure(command=lambda x=source.get("id"), btn=button: self.pre_update_source(x, btn))
#             button.pack(side="right")
#
#             installed_sources.add(source.get("id"))
#
#     def pre_update_source(self, source_id, button):
#         button.configure(state="disabled")
#         api.update_source(source_id)
#         global sources
#         sources = api.get_sources()
#         self.update_installed_listing()
#
#     def update_installed_listing(self):
#         grid_frame = self.builder.get_object("settings_sources_installed")
#         [widget.grid_forget() for row in range(1, grid_frame.grid_size()[1]) for widget in
#          grid_frame.grid_slaves(row=row)]
#         self.populate_installed()
#
#     def install_source(self, source_id, button):
#         button.configure(state="disabled")
#         api.update_source(source_id)
#         installed_sources.add(source_id)
#
#         global sources
#         sources = api.get_sources()
#         self.update_not_installed_listing()
#         self.update_installed_listing()
#
#     def update_not_installed_listing(self):
#         # Update the not installed sources
#         grid_frame = self.builder.get_object("settings_sources_not_installed")
#         [widget.grid_forget() for row in range(1, grid_frame.grid_size()[1]) for widget in
#          grid_frame.grid_slaves(row=row)]
#         self.populate_not_installed()
#
#     def pre_delete_source(self, source_id, button):
#         button.configure(state="disabled")
#         api.uninstall_source(source_id)
#         installed_sources.remove(source_id)
#         global sources
#         sources = api.get_sources()
#         self.update_installed_listing()
#         self.update_not_installed_listing()
#
#     def run(self):
#         self.mainwindow.mainloop()
#
#
# app = TkinterUI()
