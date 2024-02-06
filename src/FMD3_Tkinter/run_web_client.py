import FMD3_Tkinter
from FMD3_Tkinter.client_settings import Settings
import tkinter as tk

def save_host(dialog, entry):
    Settings().set("host", entry.get())
    Settings().save()
    dialog.destroy()

def run_web():
    from FMD3_Tkinter._api.web import WebApi
    FMD3_Tkinter.api = WebApi()
    if Settings().get("host") is None:
        dialog = tk.Tk()
        dialog.title("Settings")
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        tk.Label(dialog, text="Enter the server URL\n(schema, host and port: http://<ip>:port)").pack()
        var = tk.StringVar(value=Settings().get("host"))
        entry = tk.Entry(dialog, textvariable=var)
        entry.pack()
        tk.Button(dialog, text="Save", command=lambda: save_host(dialog, var)).pack()
        dialog.mainloop()
    from FMD3_Tkinter.app import app
    app.run()

if __name__ == '__main__':
    run_web()