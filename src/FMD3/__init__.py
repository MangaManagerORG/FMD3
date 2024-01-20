import sys
from logging import DEBUG, INFO, Handler, StreamHandler, basicConfig, addLevelName, Logger
from logging.handlers import RotatingFileHandler


umpumped_events = []

TRACE = 9


def trace(self, message, *args, **kws):
    # Yes, logger takes its '*args' as 'args'.
    self._log(TRACE, message, args, **kws)

class UmpumpedLogHandler(Handler):
    def emit(self, record):
        umpumped_events.append(record)
        ei = record.exc_info


def setup_logging(LOGFILE_PATH, level=DEBUG):
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

# def getLogger(*args,**kwargs)
addLevelName(TRACE, "TRACE")

Logger.trace = trace