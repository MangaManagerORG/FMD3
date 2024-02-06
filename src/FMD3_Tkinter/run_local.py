import FMD3_Tkinter


def run_local():
    from FMD3_Tkinter._api.local import LocalApi
    FMD3_Tkinter.api = LocalApi()
    from FMD3_Tkinter.app import app
    app.run()

if __name__ == '__main__':
    run_local()