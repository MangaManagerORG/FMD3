import logging
import sys
from logging import DEBUG, INFO, Handler, StreamHandler, basicConfig, addLevelName, Logger
from logging.handlers import RotatingFileHandler

from FMD3.constants import LOGFILE_PATH
from FMD3.core import database
from FMD3.core.settings import Settings
from FMD3.sources import get_source, load_sources

umpumped_events = []

TRACE = 9


def trace(self, message, *args, **kws):
    """
    Reports a trace. Used for spam loggings tring to trace the whole execution of a function
    Args:
        self:
        message:
        *args:
        **kws:

    Returns:

    """
    # Yes, logger takes its '*args' as 'args'.
    self._log(TRACE, message, args, **kws)


class UmpumpedLogHandler(Handler):
    def emit(self, record):
        umpumped_events.append(record)
        record.exc_info


def setup_logging(log_file_path, level=DEBUG):
    umpumped_handler = UmpumpedLogHandler(INFO)

    rotating_file_handler = RotatingFileHandler(log_file_path, maxBytes=10_000_000,
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


# def getLogger(*args,**kwargs)
addLevelName(TRACE, "TRACE")
logging.getLogger("PIL").setLevel(logging.WARNING)
Logger.trace = trace

setup_logging(LOGFILE_PATH.joinpath("log.log"), TRACE)
settings = Settings()
load_sources()
settings.save()

