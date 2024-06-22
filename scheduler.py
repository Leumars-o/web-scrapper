#!/usr/bin/python3

import intranet_login as intranet
import telegram_notify as telegram
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler

def execute_intranet():
    projects = intranet.main()
    telegram.send_notification(projects)
    job_id.remove()
    scheduler.shutdown(wait=False)

scheduler = BlockingScheduler()
job_id = scheduler.add_job(execute_intranet, 'interval', seconds = 5)

scheduler.start()
