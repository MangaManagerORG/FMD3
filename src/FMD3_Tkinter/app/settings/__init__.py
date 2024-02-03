import json
import tkinter as tk
from tkinter import ttk
from FMD3.api import update_settings
from .source_settings import SourceSettings


class Settings(SourceSettings):

    def track_setting(self, key, link_to: str | list[str] = None, section=None):
        var = self.builder.get_variable(key)
        # Set the StringVar's value to the initial value of the corresponding attribute
        var.set(self.settings["Core" if section is None else section].get(key).get("value"))
        # Set up the trace on the StringVar to call a callback when it changes
        if isinstance(link_to, list):
            for link in link_to:
                var.trace_add("write", lambda *args: self.update_attribute(key, var, link))
        else:
            var.trace_add("write", lambda *args: self.update_attribute(key, var, link_to))

    def track_setting_to_var(self, section, key, str_var):
        var = self.builder.get_variable(str_var)
        # Set the StringVar's value to the initial value of the corresponding attribute
        var.set(self.settings[section].get(key).get("value"))
        # Set up the trace on the StringVar to call a callback when it changes
        var.trace_add("write", lambda *args: self.update_attribute(section=section, key=key, string_var=var))

    def update_attribute(self, key, string_var, link_to=None, section="Core"):
        # Update the object's attribute when the StringVar changes
        new_value = string_var.get()

        if link_to:
            widget = self.builder.get_object(link_to)
            new_state = tk.NORMAL if new_value else tk.DISABLED
            widget.config(state=new_state)

        self.settings[section][key]["value"] = new_value
        print(f"setting key:{key} updated to: {new_value}")

    def apply_settings(self):
        update_settings(json.dumps(self.settings))

    def __init__(self):
        top_frame = self.builder.get_object("settings_sources_options")

        for section in self.settings:
            if section == "Core":
                continue

            # class SettingType(Enum):
            #     Bool = 0
            #     Text = 1
            #     Options = 2
            #     Number = 3
            #     Radio = 4
            #     STR_ARRAY = 5
            frame = ttk.LabelFrame(top_frame, text=section)
            frame.pack(side="top", expand=False, fill="x", anchor="n")

            for setting in self.settings[section]:
                setting_ = self.settings[section][setting]
                var_name = ("settings_vars_" + section + "_" + setting_["key"]).lower()
                ttk.Label(frame, text=setting_["name"]).pack(side="top", anchor="w")

                match setting_["type"]:
                    case 0:  # Bool
                        var = self.builder.create_variable(var_name, tk.BooleanVar)
                        var.set(setting_["value"])
                        ttk.Checkbutton(frame, variable=var).pack(side="top", anchor="w")
                    case 1:  # Text
                        var = self.builder.create_variable(var_name, tk.StringVar)
                        var.set(setting_["value"])
                        ttk.Entry(frame, textvariable=var).pack(side="top", anchor="w")
                    case 2:  # Options
                        var = self.builder.create_variable(var_name, tk.StringVar)
                        var.set(setting_["value"])
                        ttk.Combobox(frame, textvariable=var, values=setting_["values"], state="readonly").pack(
                            side="top", anchor="w")
                    case 3:  # Number
                        var = self.builder.create_variable(var_name, tk.IntVar)
                        var.set(setting_["value"])
                        ttk.Entry(frame, textvariable=var).pack(side="top", anchor="w")
                    case 4:
                        var = self.builder.create_variable(var_name, tk.StringVar)
                        var.set(setting_["value"])
                        ttk.Radiobutton(frame, variable=var, value=setting_["value"]).pack(side="top", anchor="w")

                self.track_setting_to_var(section, setting_["key"], var_name)
