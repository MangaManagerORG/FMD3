import logging
import sys
from logging import DEBUG, INFO, Handler, StreamHandler, basicConfig, addLevelName, Logger
from logging.handlers import RotatingFileHandler
from pathlib import Path

from FMD3.constants import LOGFILE_PATH, FMD3_PATH, is_development

umpumped_events = []

TRACE = 9

from .__version__ import __version__
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


def setup_logging(log_file_path, level=DEBUG):
    umpumped_handler = UmpumpedLogHandler(INFO)

    rotating_file_handler = RotatingFileHandler(log_file_path, maxBytes=10_000_000,
                                                backupCount=2)
    rotating_file_handler.setLevel(level)

    stream_handler = StreamHandler(sys.stdout)
    stream_handler.setLevel(level)
    basicConfig(level=DEBUG,
                format='%(asctime)s - [%(process)5s-%(thread)5s] - %(name)20s - %(levelname)8s - %(message)s',
                handlers=[stream_handler, rotating_file_handler, umpumped_handler]
                # filename='/tmp/myapp.log'
                )

    # logger.debug('DEBUG LEVEL - MAIN MODULE')
    # logger.info('INFO LEVEL - MAIN MODULE')
    # logger.trace('TRACE LEVEL - MAIN MODULE')


# def getLogger(*args,**kwargs)
addLevelName(TRACE, "TRACE")
logging.getLogger("PIL").setLevel(logging.WARNING)
logging.getLogger("pygubu").setLevel(logging.WARNING)
Logger.trace = trace

setup_logging(LOGFILE_PATH.joinpath("FMD3.log"), TRACE)
logger = logging.getLogger(__name__)
logger.info("Starting FMD3")
logger.info(f"FMD3 path: {FMD3_PATH.resolve().as_posix()}")
if is_development:
    logger.warning(f"Development mode. Extensions will load from '{Path(FMD3_PATH.parent.joinpath('FMD3_Extensions/extensions')).as_posix()}'" if is_development else "")
