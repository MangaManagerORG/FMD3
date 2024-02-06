import tkinter as tk
from tkinter import ttk

BALLOT_BOX = "\u2610"
BALLOT_BOX_WITH_X = "\u2612"


class TtkCheckList(ttk.Treeview):
    def __init__(self, master=None, width=200, clicked=None, separator='.',
                 unchecked=BALLOT_BOX, checked=BALLOT_BOX_WITH_X, **kwargs):
        """
        :param width: the width of the check list
        :param clicked: the optional function if a checkbox is clicked. Takes a
                        `iid` parameter.
        :param separator: the item separator (default is `'.'`)
        :param unchecked: the character for an unchecked box (default is
                          "\u2610")
        :param unchecked: the character for a checked box (default is "\u2612")

        Other parameters are passed to the `TreeView`.
        """
        if "selectmode" not in kwargs:
            kwargs["selectmode"] = "none"
        if "show" not in kwargs:
            kwargs["show"] = "tree"
        ttk.Treeview.__init__(self, master, **kwargs)
        self._separator = separator
        self._unchecked = unchecked
        self._checked = checked
        self._clicked = self.toggle if clicked is None else clicked

        self.column('#0', width=width, stretch=tk.YES)
        self.bind("<Button-1>", self._item_click, True)

    def _item_click(self, event):
        assert event.widget == self
        x, y = event.x, event.y
        element = self.identify("element", x, y)
        if element == "text":
            iid = self.identify_row(y)
            self._clicked(iid)

    def add_item(self, id, name,category="",checked=False):
        """
        Add an item to the checklist. The item is the list of nodes separated
        by dots: `Item.SubItem.SubSubItem`. **This item is used as `iid`  at
        the underlying `Treeview` level.**
        """
        try:
            parent_iid, text = id.rsplit(self._separator, maxsplit=1)
            self.insert(parent_iid, index='end', iid=id,
                        text=name + " " + self._checked if checked else self._unchecked, open=True, tags=("child",category))
        except ValueError:
            self.insert("", index='end', text=name,iid=id, open=True, tags=("parent",category))

    def is_parent(self,iid):
        return "parent" in self.item(iid, "tags")


    def toggle(self, iid):
        """
        Toggle the checkbox `iid`
        """
        if self.is_parent(iid):
            return
        text = self.item(iid, "text")
        checked = text[-1] == self._checked
        status = self._unchecked if checked else self._checked
        self.item(iid, text=text[:-1] + status)

    def checked(self, iid):
        """
        Return True if checkbox `iid` is checked
        """
        text = self.item(iid, "text")
        return text[-1] == self._checked

    def check(self, iid):
        """
        Check the checkbox `iid`
        """
        text = self.item(iid, "text")
        if text[-1] == self._unchecked:
            self.item(iid, text=text[:-1] + self._checked)

    def uncheck(self, iid):
        """
        Uncheck the checkbox `iid`
        """
        text = self.item(iid, "text")
        if text[-1] == self._checked:
            self.item(iid, text=text[:-1] + self._unchecked)