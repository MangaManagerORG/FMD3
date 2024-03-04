import multiprocessing

import FMD3_Tkinter
from FMD3_Tkinter.client_settings import Settings


def run_web():
    def save_host(dialog, entry):
        Settings().set("host", entry.get())
        Settings().save()
        dialog.destroy()

    from FMD3_Tkinter.web_api import Api
    import tkinter as tk
    FMD3_Tkinter.api = Api

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
    from FMD3_Tkinter.app.main import App
    app = App()
    # disable button as this is not useable in the api mode
    app.widget_settings_saveto_librarypath_dialog_button.pack_forget()
    app.run()

if __name__ == '__main__':
    multiprocessing.freeze_support()
    run_web()