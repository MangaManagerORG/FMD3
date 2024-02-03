from datetime import datetime

from FMD3_Tkinter.api import get_chapters
from FMD3_Tkinter.api import get_source
from FMD3_Tkinter.api import get_series


def _str_to_datetime(string):
    return datetime.strptime(string, "%Y-%m-%dT%H:%M:%S")


class Favourites:
    favourites_treeview: type[""]
    builder: type[""]

    def __init__(self):
        self.fav_tree_loaded_parents = {}
        self.favourites_treeview.tag_bind('lazy', '<<TreeviewOpen>>', self.child_opened_fav_treeview)
        self.favourites_treeview.bind('<Button-1>', self.child_opened_fav_treeview)
        self.favourites_treeview.tag_configure('favourites_child_chapters', background='#B6B7B7')
        self.load_favourites()
        self._detached_fav_filter = set()


    def load_favourites(self, series_list=get_series(sort="dateadded", order="desc")):
        for series in series_list:
            if series.get("series_id") not in self.fav_tree_loaded_parents:
                item_id = self.favourites_treeview.insert('', 'end', series.get("series_id"), text=series.get("title"),
                                                          values=(series.get("max_chapter")
                                                                  ,
                                                                  get_source(
                                                                      source_id=series.get("source_id")).get(
                                                                      "name"),
                                                                  series.get("save_to"),
                                                                  series.get("dateadded"),
                                                                  series.get("status"),
                                                                  series.get("datelastchecked"),
                                                                  series.get("datelastupdated"),
                                                                  series.get("source_id")))
            # self.favourites_treeview.insert('', 'end', f"{series.series_id}.chapters", values=(series.title, series.currentchapter))
                self.fav_tree_loaded_parents[item_id] = False
        self.fav_sort_date_added()

    def refresh_favourites(self, *_):
        self.favourites_treeview.delete(*self.favourites_treeview.get_children())
        self.load_favourites()

    def filter_favourites_treeview(self):
        tree = self.builder.get_object("favourites_treeview")
        # Get the filter text from the entry widget
        filter_text = self.builder.get_object("favourites_tab_filter_entry").get().lower()

        # Clear existing items in the tree
        children = list(self._detached_fav_filter) + list(tree.get_children())
        self._detached_fav_filter = set()

        i_r = -1
        for item_id in children:
            text = tree.item(item_id)[
                'text'].lower()  # already contains the strin-concatenation (over columns) of the row's values
            if filter_text in text:
                i_r += 1
                tree.reattach(item_id, '', i_r)
            else:
                self._detached_fav_filter.add(item_id)
                tree.detach(item_id)

    def child_opened_fav_treeview(self, *_):
        series_id = self.favourites_treeview.focus()
        if not series_id:
            return
        # Check if the item has been loaded
        if not self.fav_tree_loaded_parents.get(series_id, False):
            # Load the children of the parent item
            self.load_children(series_id, )
            # Mark the parent as loaded
            self.fav_tree_loaded_parents[series_id] = True

    def reload_fav_treeview_children(self):
        # Clear all children of the selected parent
        parent_id = self.favourites_treeview.focus()
        self.favourites_treeview.delete(*self.favourites_treeview.get_children(parent_id))

        # Reload the children for the selected parent
        self.load_children(parent_id)

    def reload_all_opened_fav_treeview_children(self):
        # Iterate over all opened parent items
        for series_id in self.fav_tree_loaded_parents:
            if series_id == '':
                continue  # skip root
            # Check if the item has been loaded
            if self.fav_tree_loaded_parents.get(series_id, False):
                # Clear all children of the parent
                self.favourites_treeview.delete(*self.favourites_treeview.get_children(series_id))

                # Reload the children for the parent
                self.load_children(series_id)

    def load_children(self, parent_id):
        # Simulate loading children from a data source
        for chapter in sorted(get_chapters(parent_id), key=lambda x: x.get("number")):
            child_id = self.favourites_treeview.insert(parent_id, 'end', text=chapter.get("title") or "",
                                                       values=(
                                                           f'Ch.{chapter["number"]} Vol.{chapter["volume"]}', "",
                                                           chapter.get("path"),
                                                           chapter.get("download_date"),
                                                           chapter.get("status"), "", "", ""),
                                                       tags=("favourites_child_chapters",))
    def fav_sort_date_added(self,*_):
        tv = self.builder.get_object("favourites_treeview")
        col = "dateadded"
        print("sadas")

        reverse = True

        l = [
            (_str_to_datetime(tv.set(k, col)), k)
            for k in tv.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        #
        #
        #
        #
        # # reverse sort next time
        # tv.heading(col, text=col, command=lambda _col=col: \
        #     treeview_sort_column(tv, _col, not reverse))