from datetime import datetime
from datetime import timedelta
from datetime import date
from subprocess import call


date = date.today()
date_format = "%Y%m%d"
step=30

for i in range(12):
    end = datetime.strftime(date, date_format)
    date = date - timedelta(days=step)
    start = datetime.strftime(date, date_format)
    cmd = "node --max-old-space-size=4096 zenbot.js sim --strategy noop poloniex.xrp-usdt " \
          "--start='{}0000' --end='{}0000' --period 1m".format(start, end)

    print(cmd)
    call(cmd, shell=True)
`
