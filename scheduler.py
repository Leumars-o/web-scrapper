#!/usr/bin/python3

import intranet_login as intranet
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler

def execute_intranet():
    intranet.main()
    job_id.remove()
    scheduler.shutdown(wait=False)

scheduler = BlockingScheduler()
job_id = scheduler.add_job(execute_intranet, 'cron', hour = 18, minute = 13)

scheduler.start()
