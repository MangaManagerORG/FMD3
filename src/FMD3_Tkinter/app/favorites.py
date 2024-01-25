from FMD3.api import get_series, get_source, get_chapters, get_series_info


class Favourites:
    favourites_treeview: type[""]
    builder: type[""]

    def __init__(self):

        self.load_favourites()

    def load_favourites(self):
        series_list = get_series()
        self.fav_tree_loaded_parents = {}

        self.favourites_treeview.tag_bind('lazy', '<<TreeviewOpen>>', self.child_opened_fav_treeview)
        self.favourites_treeview.bind('<Button-1>', self.child_opened_fav_treeview)
        self.favourites_treeview.tag_configure('favourites_child_chapters', background='#B6B7B7')
        for series in series_list:
            if series.chapters:
                max_ch = max(series.chapters, key=lambda x: x.number).number
            else:
                max_ch = None
            item_id = self.favourites_treeview.insert('', 'end', series.series_id, text=series.title, values=(max_ch
                                                                                                              ,
                                                                                                              get_source(
                                                                                                                  source_id=series.source_id).get(
                                                                                                                  "name"),
                                                                                                              "",
                                                                                                              series.status,
                                                                                                              series.dateadded,
                                                                                                              series.datelastchecked,
                                                                                                              series.datelastupdated,
                                                                                                              series.source_id))
            # self.favourites_treeview.insert('', 'end', f"{series.series_id}.chapters", values=(series.title, series.currentchapter))
            self.fav_tree_loaded_parents[item_id] = False
        self._detached_fav_filter = set()

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
        item_id = self.favourites_treeview.focus()

        # Check if the item has been loaded
        if not self.fav_tree_loaded_parents.get(item_id, False):
            # Load the children of the parent item
            self.load_children(item_id)
            # Mark the parent as loaded
            self.fav_tree_loaded_parents[item_id] = True

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



