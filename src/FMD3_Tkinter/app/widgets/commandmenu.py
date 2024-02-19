from pygubu.component.builderobject import BuilderObject
from pygubu.plugins.customtkinter.ctkbase import CTkBaseMixin, GINPUT
from pygubu.utils.datatrans import ListDTO

from customtkinter import CTkOptionMenu
from pygubu.api.v1 import register_widget, register_custom_property
from pygubu.i18n import _

_plugin_uid = "FMD3_Tkinter"
_designer_tab_label = _(_plugin_uid)


class CommandMenu(CTkOptionMenu):
    def _dropdown_callback(self, value: str):
        # self._current_value = value
        # self._text_label.configure(text=self._current_value)
        # if self._variable is not None:
        #     self._variable_callback_blocked = True
        #     self._variable.set(self._current_value)
        #     self._variable_callback_blocked = False

        if self._command is not None:
            self._command(self._current_value, value)

_list_dto = ListDTO()

class CommandMenuBO(CTkBaseMixin, BuilderObject):
    class_ = CommandMenu
    allow_bindings = False
    properties = (
        "command",
        "variable",
        "values",
        "bg_color",
        "fg_color",
        "button_color",
        "button_hover_color",
        "text_color",
        "text_color_disabled",
        "dropdown_hover_color",
        "dropdown_text_color",
        "dropdown_color",
        "dropdown_font",
        "width",
        "height",
        "corner_radius",
        "state",
        "dynamic_resizing",
        "font",
    )
    command_properties = ("command",)

    def _process_property_value(self, pname, value):
        if pname == "values":
            return _list_dto.transform(value)
        return super()._process_property_value(pname, value)

    def _code_define_callback_args(self, cmd_pname, cmd):
        return ("current_value",)

    def _code_process_property_value(self, targetid, pname, value: str):
        if pname == "values":
            return super()._process_property_value(pname, value)
        return super()._code_process_property_value(targetid, pname, value)


_ctk_values_help = _(
    "Specifies the list of values to display. "
    "In code you can pass any iterable. "
    'In Designer, a json like list: ["item1", "item2"]'
)
register_widget(
    f"{_plugin_uid}.CommandMenu",
    CommandMenuBO,
    "CommandMenu",
    ("ttk", _designer_tab_label),
    group=GINPUT,
)
register_custom_property(f"{_plugin_uid}.CommandMenu", "values", "entry", help=_ctk_values_help)
register_custom_property(
    f"{_plugin_uid}.CommandMenu",
    "state",
    "choice",
    values=("", "normal", "disabled", "readonly"),
    state="readonly"
)
