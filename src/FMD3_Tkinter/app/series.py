from io import BytesIO
from tkinter import END, NW

from PIL import ImageTk, Image

from FMD3.api import get_series_info, query_series, get_chapters, get_source_chapters, get_cover, download_chapters


def add_detail_entry(widget,data, title, data_key, tag=""):
    widget.insert("end", f"{title}:\n", "bold" + tag)
    widget.insert("end", f"{data[data_key]}\n\n")
def add_detail_entry_array(widget,data, title, data_key, tag=""):
    widget.insert("end", f"{title}:\n", "bold" + tag)
    value = data[data_key]
    if value:
        data_ = ','.join(value)
    else:
        data_ = ""
    widget.insert("end", f"{data_}\n\n")

def add_series_detail(series_detail_widget, data):
    series_detail_widget.delete('1.0', END)


    add_detail_entry(series_detail_widget, data, "Title", "title", tag="")
    add_detail_entry_array(series_detail_widget, data, "Author(s)", "authors", tag="")
    add_detail_entry_array(series_detail_widget, data, "Artist(s)", "artists", tag="")
    add_detail_entry_array(series_detail_widget, data, "Genre(s)", "genres", tag="")
    add_detail_entry(series_detail_widget, data, "Status", "status", tag="")
    add_detail_entry(series_detail_widget, data, "Summary", "description", tag="")

def list_chapters_treeview(widget, chapter_list: list, tags: tuple[str]):
    for chapter in chapter_list:
        widget.insert('', 'end', chapter.get("id"), values=(chapter.get("title"), chapter.get("volume"), chapter.get("number")), tags=tags)

class Series:
    builder: type[""]
    search_results: type[""]
    selected_source_id: type[""]

    def search_series(self, event):
        if not event.char:
            return
        ext = self.selected_source_id
        if not ext:
            return
        if not self.is_delayed_search:
            self.is_delayed_search = True
            self.mainwindow.after(1500, self.delayed_search)

    def delayed_search(self, *_):
        # ext = self.builder.get_variable("selected_source_name").get()
        source_id = self.selected_source_id
        query = self.builder.get_variable("query_stringvar").get()
        # query = "tensei"
        if not query:
            return

        series_list = query_series(self.selected_source_id,query)

        tree = self.builder.get_object("series_result")
        tree.delete(*tree.get_children())
        for result in series_list:
            self.search_results[result.get("series_id")] = result
            tree.insert('', 'end', result.get("series_id"), text=result.get("title"))


        self.is_delayed_search = False

    def select_query_result(self, event):
        search_result = self.search_results.get(event.widget.selection()[0])
        series_id = search_result.get("series_id")
        data = get_series_info(self.selected_source_id,series_id)
        if not data:
            return
        self.selected_series_id = series_id
        series_detail_widget = self.builder.get_object("series_detail")

        add_series_detail(series_detail_widget, data)
        self.load_queried_data(series_id, data)

    def load_queried_data(self, series_id, data):
        chapters_treeview = self.builder.get_object("selected_series_chapter_treeview")
        chapters_treeview.delete(*chapters_treeview.get_children())

        if dld_chapters := get_chapters(series_id):
            last_in_db = max(dld_chapters, key=lambda x: x["number"])
            list_chapters_treeview(chapters_treeview, dld_chapters, ("downloaded",))
            chapters = get_source_chapters(self.selected_source_id,series_id, last_in_db.get("number"))
            list_chapters_treeview(chapters_treeview, chapters, ("not_downloaded",))
        else:
            chapters = get_source_chapters(self.selected_source_id,series_id)
            list_chapters_treeview(chapters_treeview, chapters, ("not_downloaded",))
        self.load_queried_cover(data.get("cover_url"))

    def load_queried_cover(self, cover_url):
        # threading.Thread(target=getImageFromURL, args=(data.cover_url, self)).start()
        self.mainwindow.update()

        response = get_cover(self.selected_source_id,cover_url)
        image_ = BytesIO(response.content)
        image = Image.open(image_)
        image = image.resize((130, 200), Image.NEAREST)
        self.mainwindow.series_detail_cover_image = ImageTk.PhotoImage(image)
        print("image_loaded")

        canvas = self.builder.get_object("series_detail_cover_canvas")
        canvas.create_image(0, 0, image=self.mainwindow.series_detail_cover_image, anchor=NW)

        # canvas.itemconfig(canvas.image_id, image=self.series_detail_cover_image, state="normal")
        # canvas.config(image=self.series_detail_cover_image)
        ...

    def download_selected_chapters(self):
        chapters_treeview = self.builder.get_object("selected_series_chapter_treeview")
        to_download_ids = chapters_treeview.selection()
        to_download_series = self.selected_series_id
        download_chapters(self.selected_source_id, to_download_series, to_download_ids) # Todo save to
