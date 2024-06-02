from crontab import CronTab
cron = CronTab(user='root')
job = cron.new(command='rm -rf /opt/app/tmp/*')
job.hour.every(1)
cron.write()