import logging
import os
import signal

termination_handlers = []

logger = logging.getLogger(__name__)
def register_termination_handler(handler):
    logger.debug(f"Registered termination handler: {handler}")
    termination_handlers.append(handler)


def execute_termination_handler(*args,**kwargs):
    logger.debug(f"Executing threads and processes termination")
    for handler in termination_handlers:
        logger.debug(f"Executing termination using {handler}")
        handler(*args,**kwargs)

    os.kill(os.getpid(), signal.SIGINT)  #


signal.signal(signal.SIGINT,execute_termination_handler)