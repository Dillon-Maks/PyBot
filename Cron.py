from crontab import CronTab

cron = CronTab(user=True)
job = cron.new(command='echo Hello World!')
job.minute.every(1)

cron.write()


token = 'NzMzNDY4ODA1Njk0NzUwNzQw.XxDmKQ.SAJEVE2YO6sXsZ5up7R6TinlYt8'