import threading


class Scheduler(threading.Timer):
    def __init__(self, interval, function, args=None, kwargs=None):
        super().__init__(interval, self._wrapper, args=args, kwargs=kwargs)
        self.function = function
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        self._stopped = threading.Event()

    def every(self,interval:int=1) -> "Job":
        self.interval = interval

    def _wrapper(self):
        self.function(*self.args, **self.kwargs)
        if not self._stopped.is_set():
            self._start_timer()

    def _start_timer(self):
        self._timer = threading.Timer(self.interval, self._wrapper)
        self._timer.start()

    def start(self):
        self._start_timer()

    def stop(self):
        self._stopped.set()
        self._timer.cancel()

class Job:
    ...