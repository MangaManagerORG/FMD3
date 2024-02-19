from pygubu.component.builderobject import BuilderObject
from pygubu.plugins.customtkinter.ctkbase import CTkBaseMixin, GINPUT
from pygubu.plugins.customtkinter.widgets import CTkOptionMenuBO
from pygubu.utils.datatrans import ListDTO

from customtkinter import CTkOptionMenu
from pygubu.api.v1 import register_widget, register_custom_property
from pygubu.i18n import _

_plugin_uid = "customtkinter.FMD3_Tkinter"  # <--
_designer_tab_label = _(_plugin_uid)


class OptionMenu(CTkOptionMenu):

    def __init__(self,*args,**kwargs):
        CTkOptionMenu.__init__(self,*args,**kwargs)

    def _clicked(self,event=0):
        self._precommand(self)
        super()._clicked(event)

    def configure(self,*args, **kwargs):
        if "postcommand" in kwargs:
            self._precommand = kwargs.pop("postcommand")
        super().configure(*args, **kwargs)



class OptionMenuBO(CTkOptionMenuBO):
    class_ = OptionMenu
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
        "postcommand",  # <--
    )
    command_properties = ("postcommand","command")

    def _code_define_callback_args(self, cmd_pname, cmd):
        if cmd_pname == "postcommand":
            return ("option_menu",)
        return super()._code_define_callback_args(cmd_pname, cmd)


register_widget(
    f"{_plugin_uid}.OptionMenu",
    OptionMenuBO,
    "OptionMenu",
    ("ttk", _designer_tab_label),
    group=GINPUT,
)

register_custom_property(
    f"{_plugin_uid}.OptionMenu",
    "postcommand", "simplecommandentry")