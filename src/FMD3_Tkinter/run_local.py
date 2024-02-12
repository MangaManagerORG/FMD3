import FMD3_Tkinter
from FMD3.core.scheduler import start_scheduler_loop


def run_local():
    from FMD3_Tkinter._api.local import LocalApi
    FMD3_Tkinter.api = LocalApi()
    from FMD3_Tkinter.app import app
    start_scheduler_loop()
    app.run()

if __name__ == '__main__':
    run_local()