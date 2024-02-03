from pathlib import Path

from FMD3_Tkinter.api import get_series
from .favorites import Favourites
from .series import Series
from .settings import Settings

class App(Favourites, Series, Settings):
    # Settings stuff
    settings_libraries: dict
    def __init__(self):
        Settings.__init__(self)
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

    def series_update_final_dest(self, *_):
        default_series_downloads_path = self.builder.get_variable("default_series_downloads_path")
        series_destination_path = self.builder.get_variable("series_destination_path")
        default_lib_path = self.builder.get_variable("default_downloads_path")
        series_final_download_dest = self.builder.get_variable("series_final_download_dest")
        series_final_download_dest.set(Path(self.settings_libraries.get(default_series_downloads_path.get(),
                                                                        self.settings_libraries.get("default_lib_path",
                                                                                                    "")),
                                            series_destination_path.get()))

    def nb_tab_changed(self, event):
        match event.widget.tab(event.widget.select(), "text"):
            case "Favorites":
                self.load_favourites(get_series("dateadded", "desc", 10))
            case _:
                ...
