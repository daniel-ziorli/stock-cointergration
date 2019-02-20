from math import *
import sys
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.tsa.stattools as ts
import statistics
sys.path.append('backend')

from datacenter import *
from backend import *


def normalize(li_in):
    min_value = min(li_in)
    max_value = max(li_in)
    out = []
    for x in li_in:
        out.append((x - min_value) / (max_value - min_value))

    return out


def dist_points(x, y):
    return abs(x - y)


def avg_dist(li_1, li_2):
    dists = []
    for i in range(len(li_1)):
        dists.append(abs(li_1[i] - li_2[i]))
    return statistics.mean(dists)


def increase_month(date, num=1):
    year = int(date.split('-')[0])
    month = int(date.split('-')[1])

    month += num
    if month > 12:
        month = 1
        year += 1

    if month < 10:
        month = '0' + str(month)

    return str(year) + '-' + str(month)


def rolling_coint(x, y, n=60):

    out = []
    for i in range(n):
        out.append(None)

    for i in range(n, len(x)):
        tempx = x[i - n: i - 1]
        tempy = y[i - n: i - 1]
        pvalue = ts.coint(tempx, tempy)[1]

        out.append(pvalue)

    return out


stock = Stock(sys.argv[1])
prices = stock.get_close('2017', '2018')

f = open(sys.argv[2])
lines = f.readlines()
symbols = []
for line in lines:
    symbols.append(str(line[:-1]))

final_date = '2018-10'

'''
f = open('hrx.csv')
lines = f.readlines()
prices = []
for line in lines:
    if str(line[:-1]) != 'null':
        prices.append(float(line[:-1]))

prices = prices[len(prices) - 220:len(prices)]
print len(prices)
'''

winners = 0
lossers = 0
cash_moneyz = []


for s in symbols:

    if s == sys.argv[1].upper():
        continue

    roi = []

    start = '2017-12'
    end = '2018-01'

    stock = Stock(sys.argv[1])
    prices = stock.get_close(start, end)
    if prices == -1:
        continue

    stock2 = Stock(s)
    prices2 = stock2.get_close(start, end)
    if prices2 == -1:
        continue

    print rolling_coint(prices, prices2, 60)
    break
    run = False
    for i in stock.company_tags:
        for j in stock2.company_tags:
            if j == i:
                run = True

    if not run:
        continue

    while end != final_date:

        prices = stock.get_close(start, end)
        prices2 = stock2.get_close(start, end)

        if len(prices) != len(prices2):
            break

        pvalue = ts.coint(prices, prices2)[1]
        results = sm.OLS(prices, prices2).fit()

        trade_start = end
        trade_end = increase_month(trade_start)

        start = increase_month(start)
        end = increase_month(end)

        if pvalue < 0.001:

            prices = stock.get_close(trade_start, trade_end)
            prices2 = stock2.get_close(trade_start, trade_end)

            if len(prices) != len(prices2):
                break

            trigger = avg_dist(prices, prices2 * results.params)

            transformed_prices = prices2 * results.params

            s1 = stock_exchange(10000)
            p1 = False
            p2 = False

            # s1.stop_loss_value = -0.1
            # stopped_out = False

            for i in range(len(prices)):

                if not p2 and not p1:

                    if dist_points(prices[i], transformed_prices[i]) > trigger and prices[i] < transformed_prices[i]:
                        s1.buy(s1.capital, prices[i])
                        p1 = True

                    if dist_points(transformed_prices[i], prices[i]) > trigger and transformed_prices[i] < prices[i]:
                        s1.buy(s1.capital, prices2[i])
                        p2 = True

                if p1:
                    if dist_points(prices[i], transformed_prices[i]) < trigger or prices[i] > transformed_prices[i]:
                        p1 = False
                        s1.sell(s1.shares, prices[i])

                if p2:
                    if dist_points(prices[i], transformed_prices[i]) < trigger or prices[i] < transformed_prices[i]:
                        p2 = False
                        s1.sell(s1.shares, prices2[i])

                if p1:
                    s1.update_equity(prices[i])
                else:
                    s1.update_equity(prices2[i])

            roi.append(s1.equity[-1])

    if len(roi) > 0:
        avg_roi = statistics.mean(roi)
        print s, "mean :", avg_roi, roi
        if avg_roi < 10000:
            lossers += 1
        else:
            winners += 1

        cash_moneyz.append(avg_roi)


print winners, lossers
print statistics.mean(cash_moneyz)
