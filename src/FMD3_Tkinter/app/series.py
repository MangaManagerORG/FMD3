from io import BytesIO
from tkinter import END, NW

from PIL import ImageTk, Image
from FMD3_Tkinter import api
from FMD3_Tkinter.app.utils import get_sanitized_download


def add_detail_entry(widget, data, title, data_key, tag=""):
    widget.insert("end", f"{title}:\n", "bold" + tag)
    widget.insert("end", f"{data[data_key]}\n\n")


def add_detail_entry_array(widget, data, title, data_key, tag=""):
    widget.insert("end", f"{title}:\n", "bold" + tag)
    value = data[data_key]
    if value:
        data_ = ','.join(value)
    else:
        data_ = ""
    widget.insert("end", f"{data_}\n\n")


def add_series_detail(series_detail_widget, data):
    series_detail_widget.configure(state="normal")
    series_detail_widget.delete('1.0', END)

    add_detail_entry(series_detail_widget, data, "Title", "title", tag="")
    add_detail_entry_array(series_detail_widget, data, "Author(s)", "authors", tag="")
    add_detail_entry_array(series_detail_widget, data, "Artist(s)", "artists", tag="")
    add_detail_entry_array(series_detail_widget, data, "Genre(s)", "genres", tag="")
    add_detail_entry(series_detail_widget, data, "Status", "status", tag="")
    add_detail_entry(series_detail_widget, data, "Summary", "description", tag="")
    series_detail_widget.configure(state="disabled")

def list_chapters_treeview(widget, chapter_list: list, tags: tuple[str]):
    for chapter in chapter_list:
        widget.insert('', 'end', chapter.get("chapter_id"),
                      values=(chapter.get("title"), chapter.get("volume"), chapter.get("number")), tags=tags)


class Series:
    builder: type[""]
    search_results: type[""]
    selected_source_id: type[""]
    settings: type[""]

    def search_series(self, event):
        if not event.char:
            return
        ext = self.selected_source_id
        if not ext:
            return
        if not self.is_delayed_search:
            self.is_delayed_search = True
            self.mainwindow.after(1500, self.delayed_search)

    def series_tab_search_by_url(self,*_):
        series_url = self.builder.get_variable("series_browser_url_entry_var").get()
        if series_url:
            data = api.get_series_from_url(series_url)
            self._get_series_info(data)

    def select_query_result(self, event):
        search_result = self.search_results.get(event.widget.selection()[0])
        series_id = search_result.get("series_id")
        data = api.get_series_info(self.selected_source_id, series_id)
        self._get_series_info(data)

    def _get_series_info(self, data):

        if not data:
            return
        series_id = data["id"]
        self.selected_source_id = data.get("source_id")

        self.selected_series_id = series_id
        series_detail_widget = self.builder.get_object("series_detail")

        add_series_detail(series_detail_widget, data)
        self.load_queried_data(series_id, data)

    def delayed_search(self, *_):
        # ext = self.builder.get_variable("selected_source_name").get()
        source_id = self.selected_source_id
        query = self.builder.get_variable("query_stringvar").get()
        # query = "tensei"
        if not query:
            return

        series_list = api.query_series(self.selected_source_id, query)

        tree = self.builder.get_object("series_result")
        tree.delete(*tree.get_children())
        for result in series_list:
            self.search_results[result.get("series_id")] = result
            tree.insert('', 'end', result.get("series_id"), text=result.get("title"))

        self.is_delayed_search = False

    def load_queried_data(self, series_id, data):
        chapters_treeview = self.builder.get_object("selected_series_chapter_treeview")
        chapters_treeview.delete(*chapters_treeview.get_children())

        if dld_chapters := api.get_chapters(series_id):
            last_in_db = max(dld_chapters, key=lambda x: x["number"])
            list_chapters_treeview(chapters_treeview, dld_chapters, ("downloaded",))
            chapters = api.get_source_chapters(self.selected_source_id, series_id, last_in_db.get("number"))
            list_chapters_treeview(chapters_treeview, chapters, ("not_downloaded",))
        else:
            chapters = api.get_source_chapters(data["source_id"], series_id)
            list_chapters_treeview(chapters_treeview, chapters, ("not_downloaded",))

        frame = self.builder.get_object("frame_test_image")
        frame.load_website(data.get("cover_url"))

        output_var = self.builder.get_variable("series_destination_path")
        output_widget = self.builder.get_object("series_output_save_to_entry")
        output_lib_widget = self.builder.get_object("settings_def_series_lib_combo")

        sanitized_download = get_sanitized_download(self.settings["Core"].get("default_download_path", "")["value"],manga=data.get("title"))

        if data.get("save_to", None) is not None:
            output_widget.configure(state="disabled")
            output_lib_widget.configure(state="disabled")
            self.builder.get_variable("series_final_download_dest").set(data.get("save_to"))
            # output_var.set(data.get("save_to"))
        else:
            output_widget.configure(state="normal")
            output_lib_widget.configure(state="readonly")
            output_var.set(sanitized_download)


    def download_selected_chapters(self):
        self.builder.get_object("series_output_save_to_entry").configure(state="readonly")
        chapters_treeview = self.builder.get_object("selected_series_chapter_treeview")
        to_download_ids = chapters_treeview.selection()
        to_download_series = self.selected_series_id
        self.builder.get_object("series_output_save_to_entry").configure(state="disabled")
        self.builder.get_object("settings_def_series_lib_combo").configure(state="disabled")
        api.download_chapters(self.selected_source_id, to_download_series, to_download_ids,
                          output_path=self.builder.get_variable("series_final_download_dest").get())  # Todo save to
