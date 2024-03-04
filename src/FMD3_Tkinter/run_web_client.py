import multiprocessing

import FMD3_Tkinter

def run_web():
    from FMD3_Tkinter.web_api import Api
    FMD3_Tkinter.api = Api

    from FMD3_Tkinter.app.main import App
    app = App()
    # disable button as this is not useable in the api mode
    app.widget_settings_saveto_librarypath_dialog_button.pack_forget()
    app.run()

if __name__ == '__main__':
    multiprocessing.freeze_support()
    run_web()