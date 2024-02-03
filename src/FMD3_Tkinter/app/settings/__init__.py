import json
import tkinter as tk
from FMD3.api import update_settings
from .source_settings import SourceSettings

class Settings(SourceSettings):
    def track_setting(self, key, link_to: str | list[str] = None):
        var = self.builder.get_variable(key)
        # Set the StringVar's value to the initial value of the corresponding attribute
        var.set(self.settings["Core"].get(key).get("value"))
        # Set up the trace on the StringVar to call a callback when it changes
        if isinstance(link_to, list):
            for link in link_to:
                var.trace_add("write", lambda *args: self.update_attribute(key, var, link))
        else:
            var.trace_add("write", lambda *args: self.update_attribute(key, var, link_to))

    def update_attribute(self, key, string_var, link_to=None):
        # Update the object's attribute when the StringVar changes
        new_value = string_var.get()

        if link_to:
            widget = self.builder.get_object(link_to)
            new_state = tk.NORMAL if new_value else tk.DISABLED
            widget.config(state=new_state)

        self.settings["Core"][key]["value"] = new_value
        print(f"setting key:{key} updated to: {new_value}")

    def apply_settings(self):
        update_settings(json.dumps(self.settings))