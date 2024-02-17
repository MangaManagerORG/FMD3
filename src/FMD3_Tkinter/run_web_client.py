import requests

import FMD3_Tkinter
from FMD3_Tkinter.client_settings import Settings
import tkinter as tk

def save_host(dialog, entry):
    Settings().set("settings_client_host_var", entry.get())
    Settings().save()
    dialog.destroy()

def run_web():
    from FMD3_Tkinter._api.web import WebApi
    FMD3_Tkinter.api = WebApi()
    if Settings().get("settings_client_host_var") is None:
        dialog = tk.Tk()
        dialog.title("Settings")
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        tk.Label(dialog, text="Enter the server URL\n(schema, host and port: http://<ip>:port)").pack()
        var = tk.StringVar(value=Settings().get("settings_client_host_var"))
        entry = tk.Entry(dialog, textvariable=var)
        entry.pack()
        tk.Button(dialog, text="Save", command=lambda: save_host(dialog, var)).pack()
        dialog.mainloop()

    # Try to connect
    try:
        r = requests.get(Settings().get("settings_client_host_var"))
        r.raise_for_status()
    except requests.exceptions.ConnectionError:
        raise ConnectionError("Could not connect to server")


    # from FMD3_Tkinter.app import app
    from FMD3_Tkinter.app.main import Fmd3App
    app = Fmd3App()
    app.run()


if __name__ == '__main__':
    run_web()