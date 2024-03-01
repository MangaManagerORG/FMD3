import logging
import os
import signal

termination_handlers = []


def register_termination_handler(handler):
    logging.getLogger().debug(f"Registered termination handler: {handler}")
    termination_handlers.append(handler)


def execute_termination_handler(*args,**kwargs):
    logging.getLogger("FMD3.core").debug(f"Executing threads and processes termination")
    for handler in termination_handlers:
        logging.getLogger("FMD3.core").debug(f"Executing termination using {handler}")
        handler(*args,**kwargs)

    os.kill(os.getpid(), signal.SIGINT)  #


signal.signal(signal.SIGINT,execute_termination_handler)