from crontab import CronTab
import datetime

my_cron = CronTab(user='tianwang')

# iterate through crontab of the user
#for job in my_cron:
#	print(job)

# createing a new cron job
timenow = datetime.datetime.now()
job = my_cron.new(command='python /home/tianwang/Data/InstaPy/quickstart.py >> /home/tianwang/Data/InstaPy/logs/')

