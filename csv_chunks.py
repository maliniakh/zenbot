from datetime import datetime
from datetime import timedelta
from datetime import date
from subprocess import call
from subprocess import check_output


date_format = "%Y%m%d"
# todo: sparametryzowac
step = 30  # w dniach
steps = 1

# todo: sparametryzowac
pairs = open("pairs/binance").read().splitlines()

for pair in pairs:
    date = date.today()

    for i in range(steps):
        end = datetime.strftime(date, date_format)
        date = date - timedelta(days=step)
        start = datetime.strftime(date, date_format)
        cmd = "node --max-old-space-size=4096 zenbot.js sim --strategy noop {} " \
              "--start='{}0000' --end='{}0000' --period 1m".format(pair, start, end)

        print(cmd)
        call(cmd, shell=True)

        # todo: zamiast robic ls lepiej po prostu ustalic nazwy plikow
        ls = check_output('ls -t /home/maliniak/code/zenbot/simulations/*{}*.csv'.format(pair), shell=True)
        print(ls)
        ls = check_output('ls -t /home/maliniak/code/zenbot/simulations/sim_result*{}*.csv | head -{}'.format(pair, steps),
                          shell=True)\
            .decode("utf-8")
        ls = str.replace(ls, "\n", " ")
        call("cat {} > simulations/merged-{}.csv".format(ls, pair), shell=True)
        # usuniecie headerow z csvow oprocz pierwszego
        call("sed '2,${{ /trend/d }}' simulations/merged-{}.csv | sponge simulations/merged-{}.csv".format(pair, pair), shell=True)

