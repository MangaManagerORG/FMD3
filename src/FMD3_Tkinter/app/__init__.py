import json
import tkinter as tk
from pathlib import Path

from FMD3.api import update_settings
from .favorites import Favourites
from .series import Series


class App(Favourites, Series):

    # Settings stuff
    settings_libraries: dict
    def track_setting(self, key, link_to: str | list[str] = None):
        var = self.builder.get_variable(key)
        # Set the StringVar's value to the initial value of the corresponding attribute
        var.set(self.settings["Core"].get(key).get("value"))
        # Set up the trace on the StringVar to call a callback when it changes
        if isinstance(link_to, list):
            for link in link_to:
                var.trace_add("write", lambda *args: self.update_attribute(key, var, link))
        else:
            var.trace_add("write", lambda *args: self.update_attribute(key, var, link_to))

    def update_attribute(self, key, string_var, link_to=None):
        # Update the object's attribute when the StringVar changes
        new_value = string_var.get()

        if link_to:
            widget = self.builder.get_object(link_to)
            new_state = tk.NORMAL if new_value else tk.DISABLED
            widget.config(state=new_state)

        self.settings["Core"][key]["value"] = new_value
        print(f"setting key:{key} updated to: {new_value}")

    def apply_settings(self):
        update_settings(json.dumps(self.settings))

    def add_library_to_treeview(self, *_):
        alias = self.builder.get_variable("settings_lib_alias_entry").get()
        path = self.builder.get_variable("settings_lib_path_entry").get()

        self.settings_libraries[alias] = path

        tree = self.builder.get_object("settings_libraries_treeview")

        tree.insert('', 'end', path, values=(alias, path))
        self.settings["Core"].get("libraries_alias_paths_list")["value"].append({"alias": alias, "path": path})
        print("sads")

    def settings_load_libs_from_treeview(self):
        libs = self.settings_libraries
        tree = self.builder.get_object("settings_libraries_treeview")

        lib_selector_combo = self.builder.get_object("settings_def_lib_combo")
        series_lib_selector_combo = self.builder.get_object("settings_def_series_lib_combo")

        lib_selector_combo['values'] = list(libs)
        series_lib_selector_combo['values'] = list(libs)

    def settings_load_save_to_treeview_from_settings(self):
        tree = self.builder.get_object("settings_libraries_treeview")
        for lib in self.settings["Core"].get("libraries_alias_paths_list")["value"]:
            # libs.append(lib["alias"] + " - " + lib["path"])
            self.settings_libraries[lib["alias"]] = lib["path"]
            tree.insert('', 'end', lib["path"], values=(lib["alias"], lib["path"]))
    def series_update_final_dest(self,*_):
        default_series_downloads_path = self.builder.get_variable("default_series_downloads_path")
        series_destination_path = self.builder.get_variable("series_destination_path")
        default_lib_path = self.builder.get_variable("default_downloads_path")
        series_final_download_dest = self.builder.get_variable("series_final_download_dest")
        series_final_download_dest.set(Path(self.settings_libraries.get(default_series_downloads_path.get(),self.settings_libraries.get("default_lib_path","")),series_destination_path.get()))
