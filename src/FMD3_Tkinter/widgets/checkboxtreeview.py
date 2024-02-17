import os
from tkinter import ttk

from PIL import ImageTk, Image

from pygubu.api.v1 import register_widget
from pygubu.i18n import _
from pygubu.plugins.ttk.ttkstdwidgets import TTKTreeviewBO, TTKTreeviewColumnBO
from pygubu.plugins.pygubu.scrollbarhelper import TTKSBHelperBO
from ttkwidgets import CheckboxTreeview as CBT
from ttkwidgets.checkboxtreeview import IM_TRISTATE
from ttkwidgets.utilities import get_assets_directory

_plugin_uid = "FMD3_Tkinter"
_designer_tab_label = _("FMD3_Tkinter")
from pathlib import Path
assets_path = Path(Path(__file__).parent.parent,"assets")
IM_CHECKED = Path(assets_path,"checked.png").resolve()       # These three checkbox icons were isolated from
IM_UNCHECKED = Path(assets_path, "unchecked.png").resolve()      # These three checkbox icons were isolated from

class CheckboxTreeview(CBT):
    def __init__(self, master=None, **kw):
        """
        Create a CheckboxTreeview.

        :param master: master widget
        :type master: widget
        :param kw: options to be passed on to the :class:`ttk.Treeview` initializer
        """
        ttk.Treeview.__init__(self, master, style='Checkbox.Treeview', **kw)
        # style (make a noticeable disabled style)
        style = ttk.Style(self)
        style.map("Checkbox.Treeview",
                  fieldbackground=[("disabled", '#E6E6E6')],
                  foreground=[("disabled", 'gray40')],
                  background=[("disabled", '#E6E6E6')])
        # checkboxes are implemented with pictures
        self.im_checked = ImageTk.PhotoImage(Image.open(IM_CHECKED), master=self)
        self.im_unchecked = ImageTk.PhotoImage(Image.open(IM_UNCHECKED), master=self)
        self.im_tristate = ImageTk.PhotoImage(Image.open(IM_TRISTATE), master=self)
        self.tag_configure("unchecked", image=self.im_unchecked)
        self.tag_configure("tristate", image=self.im_tristate)
        self.tag_configure("checked", image=self.im_checked, foreground="#3484F0", background="#BBCFED")

        # check / uncheck boxes on click
        self.bind("<Button-1>", self._box_click, True)
    def check_all(self):
        print("supered")
        super().check_all()

    def _box_click(self, event):
        """Check or uncheck box when clicked."""
        x, y, widget = event.x, event.y, event.widget
        elem = widget.identify("element", x, y)
        # if "image" in elem:

        # a box was clicked
        item = self.identify_row(y)
        if self.tag_has("unchecked", item) or self.tag_has("tristate", item):
            self._check_ancestor(item)
            self._check_descendant(item)
        else:
            self._uncheck_descendant(item)
            self._uncheck_ancestor(item)

class CheckboxTreeviewBO(TTKTreeviewBO):
    class_ = CheckboxTreeview
    allowed_children = ("ttk.Treeview.Column",)


_builder_uid = f"{_plugin_uid}.CheckboxTreeview"
register_widget(
    _builder_uid,
    CheckboxTreeviewBO,
    "CheckboxTreeview",
    ("ttk", _designer_tab_label),
)

TTKSBHelperBO.add_allowed_child(_builder_uid)
TTKTreeviewColumnBO.add_allowed_parent(_builder_uid)
