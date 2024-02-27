import logging
import threading
from time import sleep

import schedule
from FMD3.core.settings import Settings
from FMD3.core.settings import Keys
from FMD3.core.updater import new_chapters_finder

logger = logging.getLogger(__name__)
def start_fav_scan_schedule():
    minutes = Settings().get(Keys.CHECK_NEW_FAV_CHAPTERS_INTERVAL_MINUTES)
    # minutes = 2
    if not minutes:
        logger.error("NO MINUTES DEFINED")
        return
    minutes = int(minutes)
    schedule.every(minutes).seconds.do(new_chapters_finder).run()


def run_scheduler(run_pending_every=120):
    logger.info("Started scheduler")
    start_fav_scan_schedule()
    while 1:
        schedule.run_pending()
        sleep(run_pending_every)

def start_scheduler_loop():
    threading.Thread(target=run_scheduler).start()