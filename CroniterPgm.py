from crontab import CronTab

# Importing OS module
import os
# Python get home directory using os module
dir = '/home/pi/Downloads/Advertisements'
print("CWD:", dir)
userName = str(os.path.expanduser("~")).split('/')[-1]
print("userName:", userName)
from datetime import datetime
dtime = str(datetime.now())

my_crons = CronTab(user=userName)
for job in my_crons:
    sch = job.schedule(date_from=datetime.now())
    print(sch.get_next())
    
    
# to get the job frequency, will return the number of times the job gets executed in a year.

my_cron = CronTab(user=userName)
for job in my_cron:
    print("per Year:", job.frequency())
    print("per Hour:", job.frequency_per_hour())