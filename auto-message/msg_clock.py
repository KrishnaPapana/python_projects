from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from auto_msg import auto_message

sched = BlockingScheduler()

auto_message()
sched.add_job(auto_message, 'interval', hours=12)

sched.start()