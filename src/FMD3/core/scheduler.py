import logging
import threading
import time

import schedule

from FMD3.core import register_termination_handler
from FMD3.core.settings import Settings
from FMD3.core.settings import Keys
from FMD3.core.updater import new_chapters_finder

logger = logging.getLogger(__name__)

_stopped = threading.Event()


class RepeatingTimer(threading.Timer):
    def __init__(self, interval, function, args=None, kwargs=None):
        # signal.signal(signal.SIGINT, self.stop)
        super().__init__(interval, function, args=args, kwargs=kwargs)
        self.function = function
        self.args = args if args is not None else ()
        self.kwargs = kwargs if kwargs is not None else {}
        self._running = False


    def _wrapper(self):
        self._running = True

        self.function(*self.args, **self.kwargs)
        self._running = False
        if not _stopped.is_set():
            while self._running:
                time.sleep(5)
            if not _stopped.is_set():
                self._timer = threading.Timer(self.interval, self._wrapper)
                self._timer.start()
        else:
            self.stop()

    def start(self):
        self._timer = threading.Timer(self.interval, self._wrapper)
        self._timer.start()

    def stop(self,*_):
        logger.info("Shutting down [Scheduler]")
        _stopped.set()
        self.cancel()


def start_scheduler_loop():
    minutes = Settings().get(Keys.CHECK_NEW_FAV_CHAPTERS_INTERVAL_MINUTES) or 3
    time_in_seconds = minutes * 60

    logger.info("Started scheduler")
    timer = RepeatingTimer(
        interval=time_in_seconds,
        function=new_chapters_finder)
    timer.start()
    register_termination_handler(timer.stop)
