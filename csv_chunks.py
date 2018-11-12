from datetime import datetime
from datetime import timedelta
from datetime import date
from subprocess import call
from subprocess import check_output


date = date.today()
date_format = "%Y%m%d"
step = 1
steps = 5

for i in range(steps):
    end = datetime.strftime(date, date_format)
    date = date - timedelta(days=step)
    start = datetime.strftime(date, date_format)
    cmd = "node --max-old-space-size=4096 zenbot.js sim --strategy noop poloniex.xrp-usdt " \
          "--start='{}0000' --end='{}0000' --period 1m".format(start, end)

    print(cmd)
    call(cmd, shell=True)

ls = check_output('ls -t /home/maliniak/code/zenbot/simulations/*.csv | head -{}'.format(steps), shell=True)\
    .decode("utf-8")
ls = str.replace(ls, "\n", " ")
call("cat {} > simulations/merged.csv".format(ls), shell=True)
call("sed '2,${ /trend/d }' simulations/merged.csv | sponge simulations/merged.csv", shell=True)
print(ls)

