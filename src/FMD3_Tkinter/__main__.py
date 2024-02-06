import argparse
import tkinter as tk
import FMD3_Tkinter
from FMD3_Tkinter.client_settings import Settings

def save_host(dialog, entry):
    Settings().set("host", entry.get())
    Settings().save()
    dialog.destroy()

def main():
    parser = argparse.ArgumentParser(description='Specify API type.')
    parser.add_argument('--web', action='store_true', help='Use WebApi')
    parser.add_argument('--local', action='store_true', help='Use LocalApi')
    args = parser.parse_args()

    if args.web:
        from FMD3_Tkinter._api.web import WebApi
        FMD3_Tkinter.api = WebApi()
        if Settings().get("host") is None:

            dialog = tk.Tk()
            dialog.title("Settings")
            dialog.geometry("300x200")
            dialog.resizable(False, False)
            tk.Label(dialog, text="Enter the server URL\n(schema, host and port: http://<ip>:port)").pack()
            var = tk.StringVar(value=Settings().get("host"))
            entry = tk.Entry(dialog,textvariable=var)
            entry.pack()
            tk.Button(dialog, text="Save", command=lambda: save_host(dialog, var)).pack()
            dialog.mainloop()
    # elif args.local:

    #     FMD3_Tkinter.api = FMD3_Tkinter.LocalApi()
    else:
        from FMD3_Tkinter._api.local import LocalApi
        FMD3_Tkinter.api = LocalApi()

    from FMD3_Tkinter.app import app
    app.run()


if __name__ == "__main__":
    main()
