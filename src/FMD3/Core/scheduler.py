from time import sleep

import schedule
from FMD3.Core.settings import Settings
from FMD3.Core.settings.Keys import Updates
from FMD3.Core.updater import new_chapters_finder
from FMD3.Sources import get_sources_list
from FMD3.Core import database as db

def start_fav_scan_schedule():
    minutes = Settings().get(Updates, Updates.CHECK_NEW_FAV_CHAPTERS_INTERVAL_MINUTES)
    # minutes = 2
    if not minutes:
        print("NO MINUTES DEFINED")
        return
    minutes = int(minutes)
    schedule.every(minutes).seconds.do(new_chapters_finder).run()

def run_scheduler(run_pending_every=5):
    while 1:
        schedule.run_pending()
        sleep(run_pending_every)
