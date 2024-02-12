import logging
from time import sleep

import schedule
from FMD3.core.settings import Settings
from FMD3.core.settings import Keys
from FMD3.core.updater import new_chapters_finder


def start_fav_scan_schedule():
    minutes = Settings().get(Keys.CHECK_NEW_FAV_CHAPTERS_INTERVAL_MINUTES)
    # minutes = 2
    if not minutes:
        print("NO MINUTES DEFINED")
        return
    minutes = int(minutes)
    schedule.every(minutes).seconds.do(new_chapters_finder).run()


def run_scheduler(run_pending_every=120):
    logging.getLogger(__name__).info("Started scheduler")
    while 1:
        schedule.run_pending()
        sleep(run_pending_every)

