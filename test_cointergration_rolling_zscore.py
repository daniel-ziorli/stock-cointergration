import random
from math import *
import sys
import matplotlib.pyplot as plt
import statistics
import statsmodels.api as sm
import statsmodels.tsa.stattools as ts
sys.path.append('backend')

from datacenter import *
from backend import *


def normalize(li_in):
    if li_in == -1 or len(li_in) == 0:
        return -1
    min_value = min(li_in)
    max_value = max(li_in)
    if max_value - min_value == 0:
        return -1
    out = []
    for x in li_in:
        out.append((x - min_value) / (max_value - min_value))

    return out


def dist_points(x, y):
    return (x - y)**2


def uclid_dist(li_1, li_2):
    if len(li_1) != len(li_2):
        return -1
    summation = 0
    for i in range(len(li_1)):
        summation += dist_points(li_1[i], li_2[i])
    return sqrt(summation)


def zscore(series):
    return (series - statistics.mean(series)) / statistics.stdev(series)


def rolling_beta(x, y, window=30):
    rtn = []
    for i in range(window):
        rtn.append(None)
    for i in range(window, len(x)):
        tempx = x[i - window:i]
        tempy = y[i - window:i]
        results = sm.OLS(tempy, tempx).fit()
        rtn.append(results.params)

    return rtn


def rolling_stdev(series, window=30):
    rtn = []
    for i in range(window):
        rtn.append(None)
    for i in range(window, len(series)):
        if series[i - window] is None:
            rtn.append(None)
            continue
        temp = series[i - window:i]
        dev = statistics.stdev(temp)
        rtn.append(dev)

    return rtn


def rolling_zscore(short_period, long_period, stdev, window=30):
    rtn = []
    for i in range(0, len(short_period)):
        if stdev[i] is None:
            rtn.append(None)
            continue
        temp = (short_period[i] - long_period[i]) / stdev[i]
        rtn.append(temp)
    return rtn


def add_month(date):
    year = date.split('-')[0]
    month = int(date.split('-')[1])
    month += 1
    if month < 10:
        return year + '-0' + str(month)
    else:
        return year + '-' + str(month)


start_date = '2017-01'
end_date = '2018-01'

stock = Stock(sys.argv[1])
prices = stock.get_close(start_date, end_date)
stock2 = Stock(sys.argv[2])
prices2 = stock2.get_close(start_date, end_date)

print ts.coint(prices, prices2)
results = sm.OLS(prices2, prices).fit()

rolling_b_1 = rolling_beta(prices, prices2, 1)
rolling_b_30 = rolling_beta(prices, prices2, 30)

spread_1 = []
for i in range(1):
    spread_1.append(None)
for i in range(1, len(prices)):
    spread_1.append(float(prices2[i] - prices[i] * rolling_b_1[i]))

spread_30 = []
for i in range(30):
    spread_30.append(None)
for i in range(30, len(prices)):
    spread_30.append(float(prices2[i] - prices[i] * rolling_b_30[i]))

print spread_30
std_30 = rolling_stdev(spread_30, 30)
print len(spread_1), len(spread_30), len(std_30)
rolling_zscore_30_1 = rolling_zscore(spread_1, spread_30, std_30, 30)

e = stock_exchange(10000)
for i in range(len(rolling_zscore_30_1)):
    if rolling_zscore_30_1[i] is None:
        continue

    if rolling_zscore_30_1[i] < -1:
        e.buy(e.capital, prices2[i])
    if rolling_zscore_30_1[i] >= 0:
        e.sell(e.shares, prices2[i])

print e.capital
'''
f = open(sys.argv[2])
lines = f.readlines()
symbols = []
for line in lines:
    symbols.append(str(line[:-1]))


for s in symbols:
    ud_l = []
    start_date = '2017-01'
    end_date = '2018-01'

    stock = Stock(sys.argv[1])
    prices = stock.get_close(start_date, end_date)
    stock2 = Stock(s)
    prices2 = stock2.get_close(start_date, end_date)

    prices = normalize(prices)
    if prices == -1:
        continue
    prices2 = normalize(prices2)
    if prices2 == -1:
        continue

    ud = uclid_dist(prices, prices2)
    if ud == -1:
        continue
    if ud < 2:
        print s + ': ' + str(ud)
'''
