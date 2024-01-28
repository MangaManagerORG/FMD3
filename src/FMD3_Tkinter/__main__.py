import json
import pathlib
import tkinter as tk
import pygubu
from FMD3_Tkinter.app import App
from FMD3.api import get_sources, get_series_info, get_settings, update_settings

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "ui_test.ui"

sources = get_sources()


class Source_():
    def __init__(self, id, name):
        self.id_ = id
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class TkinterUI(App):

    def __init__(self, master=None, translator=None):

        self.settings = json.loads(get_settings())

        self.builder = builder = pygubu.Builder(translator)
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: tk.Tk = builder.get_object("tk1", master)
        self.favourites_treeview = self.builder.get_object("favourites_treeview")
        builder.connect_callbacks(self)
        s = get_sources()
        builder.get_object("source_selector_combobox").config(values=[s["name"] for s in sources])

        self.selected_source_id = None
        self.search_results = {}
        self.is_delayed_search = False
        self.builder.get_object("series_detail").tag_configure("bold", font="Helvetica 12 bold")
        chapters_treeview = self.builder.get_object("selected_series_chapter_treeview")
        chapters_treeview.tag_configure('downloaded', background='lime')
        chapters_treeview.tag_configure('not_downloaded', background='grey')
        self.series_detail_cover_image = None
        self.mainwindow.state('zoomed')

        self.track_setting("default_downloads_path")
        # self.track_checkbox("replace_unicode_char_checkbox","replace_unicode_char_with_entry")
        self.track_setting("replace_unicode", "replace_unicode_char_with_entry")
        self.track_setting("replace_unicode_with")

        self.track_setting("generate_series_folder","manga_folder_name_entry")
        self.track_setting("series_folder_name")

        # self.track_setting("remove_manga_name_from_chapter_name")
        self.track_setting("chapter_name")

        self.track_setting("rename_chapter_digits_volume","rename_volume_digits_spinbox")
        self.track_setting("rename_chapter_digits_chapter","rename_chapter_digits_spinbox")
        self.track_setting("rename_chapter_digits_volume_value")
        self.track_setting("rename_chapter_digits_chapter_value")



        super().__init__()

    def on_source_selected(self, *_):

        combo = self.builder.get_object("source_selector_combobox")
        selected_index = combo.current()
        source = sources[selected_index]
        self.selected_source_id = source.get("id")
        # selected_value = values[selected_index][1]  # Extract the second element of the tuple

    # Cross tabs methods
    def show_selected_in_series_tab(self, *_):
        tree = self.builder.get_object("favourites_treeview")

        if tree.selection():
            series_id = tree.selection()[0]
            values = tree.item(series_id, "values")
            if not self.selected_source_id:
                self.selected_source_id = values[7]
            data = get_series_info(values[7], tree.selection()[0])
            if data:
                series_result_tree = self.builder.get_object("series_result")
                series_result_tree.delete(*series_result_tree.get_children())
                self.load_queried_data(series_id, data)
                self.builder.get_object("notebook_widget").select(1)

    def run(self):
        self.mainwindow.mainloop()

    def track_setting(self, key, link_to=None):
        var = self.builder.get_variable(key)
        # Set the StringVar's value to the initial value of the corresponding attribute
        var.set(self.settings.get(key).get("value"))
        # Set up the trace on the StringVar to call a callback when it changes
        var.trace_add("write", lambda *args: self.update_attribute(key, var, link_to))

    def update_attribute(self, key, string_var, link_to=None):
        # Update the object's attribute when the StringVar changes
        new_value = string_var.get()

        if link_to:
            widget = self.builder.get_object(link_to)
            new_state = tk.NORMAL if new_value else tk.DISABLED
            widget.config(state=new_state)

        self.settings[key]["value"] = new_value
        print(f"setting key:{key} updated to: {new_value}")

    def apply_settings(self):
        update_settings(json.dumps(self.settings))


if __name__ == "__main__":
    app = TkinterUI()
    app.run()
