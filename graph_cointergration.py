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


print sys.argv[1]
print sys.argv[2]

s = '2016'
e = '2019'

stock = Stock(sys.argv[1])
prices = stock.get_close(s, e)
stock2 = Stock(sys.argv[2])
prices2 = stock2.get_close(s, e)

'''
f = open('hrx.csv')
lines = f.readlines()
prices = []
for line in lines:
    if str(line[:-1]) != 'null':
        prices.append(float(line[:-1]))
prices = prices[len(prices) - 220:len(prices)]
'''

print ts.coint(prices, prices2)
results = sm.OLS(prices, prices2).fit()

trigger = avg_dist(prices, prices2 * results.params)

transformed_prices = prices2 * results.params

s1 = stock_exchange(10000)
p1 = False
p2 = False

for i in range(len(prices)):

    if dist_points(prices[i], transformed_prices[i]) > trigger and prices[i] < transformed_prices[i] and not p2 and not p1:
        s1.buy(s1.capital, prices[i])
        print 'bought', sys.argv[1], str(prices[i])
        p1 = True

    if dist_points(transformed_prices[i], prices[i]) > trigger and transformed_prices[i] < prices[i] and not p1 and not p2:
        s1.buy(s1.capital, prices2[i])
        print 'bought', sys.argv[2], str(prices2[i])
        p2 = True

    if p1:
        if dist_points(prices[i], transformed_prices[i]) < 0.1 or prices[i] > transformed_prices[i]:
            p1 = False
            s1.sell(s1.shares, prices[i])
            print 'sold', sys.argv[1], str(prices[i])

    if p2:
        if dist_points(prices[i], transformed_prices[i]) < 0.1 or prices[i] < transformed_prices[i]:
            p2 = False
            s1.sell(s1.shares, prices2[i])
            print 'sold', sys.argv[2], str(prices2[i])

    if p1:
        s1.update_equity(prices[i])
    else:
        s1.update_equity(prices2[i])


print s1.equity[-1]

plt.plot(prices, label=sys.argv[1])
plt.plot(prices2 * results.params, label=sys.argv[2])

plt.legend()
plt.show()
