from crontab import CronTab
cron = CronTab(user='root')
job = cron.new(command='rm -rf /python-docker/tmp/*')
job.setall('2 10 * * *')
cron.write()