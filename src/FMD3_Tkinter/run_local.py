import multiprocessing
import os
import signal

import FMD3.core
import FMD3_Tkinter
from FMD3.core import register_termination_handler


def run_local():
    # from FMD3_Tkinter._api.local import LocalApi
    from FMD3.api.api import Api
    FMD3_Tkinter.api = Api
    from FMD3_Tkinter.app.main import App
    from FMD3.core.scheduler import start_scheduler_loop
    start_scheduler_loop()
    app = App()
    app.mainwindow.protocol("WM_DELETE_WINDOW",FMD3.core.execute_termination_handler)
    app.run()
if __name__ == '__main__':
    multiprocessing.freeze_support()
    run_local()