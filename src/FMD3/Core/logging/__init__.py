import sys
from logging import *
from logging.handlers import RotatingFileHandler

TRACE = 9
import

def trace(self, message, *args, **kws):
    # Yes, logger takes its '*args' as 'args'.
    self._log(TRACE, message, args, **kws)

def add_trace_level():
    TRACE = 9
    addLevelName(TRACE, "TRACE")

    Logger.trace = trace

class UmpumpedLogHandler(Handler):
    def emit(self, record):
        umpumped_events.append(record)
        ei = record.exc_info

def setup_logging(LOGFILE_PATH,level=DEBUG):
    umpumped_events = []

    umpumped_handler = UmpumpedLogHandler(INFO)

    rotating_file_handler = RotatingFileHandler(LOGFILE_PATH, maxBytes=10_000_000,
                                                backupCount=2)
    rotating_file_handler.setLevel(level)

    stream_handler = StreamHandler(sys.stdout)
    stream_handler.setLevel(level)
    basicConfig(level=DEBUG,
                    format='%(asctime)s - %(name)20s - %(levelname)8s - %(message)s',
                    handlers=[stream_handler, rotating_file_handler, umpumped_handler]
                    # filename='/tmp/myapp.log'
                    )



    # logger.debug('DEBUG LEVEL - MAIN MODULE')
    # logger.info('INFO LEVEL - MAIN MODULE')
    # logger.trace('TRACE LEVEL - MAIN MODULE')