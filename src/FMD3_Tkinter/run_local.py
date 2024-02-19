import FMD3_Tkinter
from FMD3.core.scheduler import start_scheduler_loop



def run_local():
    # from FMD3_Tkinter._api.local import LocalApi
    from FMD3.api.api import Api
    FMD3_Tkinter.api = Api

    from FMD3_Tkinter.app.main import App
    start_scheduler_loop()
    App().run()
if __name__ == '__main__':
    run_local()