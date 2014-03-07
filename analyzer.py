#!/usr/bin/env python

from scipy.stats import pearsonr 
from scipy.signal import correlate
from pylab import show, plot, figure, title, xlabel, ylabel, legend, yticks, xticks
from numpy import linspace, sin, cos, pi, array, diff, real, imag
from numpy.fft import fft, rfft
import csv
import dateutil
from datetime import datetime

def normalize(a):
    b = []
    for x in a:
        b.append((x - min(a)) / (max(a)-min(a)))
    return b 

def totimestamp(t):
    epoch = datetime(1970, 1, 1)
    diff = t-epoch
    return diff.days * 24 * 3600 + diff.seconds

def load_stock(name):
    data = []
    with open('./stocks/%s.csv' % (name)) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            t = dateutil.parser.parse(row[0])
            data.append([ totimestamp(t), float(row[1]), float(row[2]) ])
    return data

def load_commodity(name):
    data = []
    with open('./commodities/%s.csv' % (name)) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            t = dateutil.parser.parse(row[0])
            data.append([ totimestamp(t), float(row[1]) ])
    return data


def keys(n):
    return map(lambda x: x[0], n)
def values(n):
    return map(lambda x: x[1], n)

start_t = 1078444800 # When the stock market started.

oil = load_commodity('OIL')
oil = filter(lambda x: x[0] >= start_t, oil)

aapl = load_stock('AAPL')
aapl = filter(lambda x: x[0] >= start_t and x[0] in keys(oil) , aapl)

bac = load_stock('BAC')
bac = filter(lambda x: x[0] >= start_t and x[0] in keys(oil), bac)

xom = load_stock('XOM')
xom = filter(lambda x: x[0] >= start_t and x[0] in keys(oil), xom)

sd = load_stock('SD')
sd = filter(lambda x: x[0] >= start_t and x[0] in keys(oil), sd)

rdsa = load_stock('RDS-A')
rdsa = filter(lambda x: x[0] >= start_t and x[0] in keys(oil), rdsa)


figure()
title('Graph of the relationship between stocks and commodities')

plot(keys(aapl), values(aapl), '--m', label='AAPL')
plot(keys(bac), values(bac), '--k', label='BAC')
plot(keys(xom), values(xom), '-g', label='XOM')
plot(keys(sd), values(sd), '-b', label='SD')
plot(keys(rdsa), values(rdsa), '-c', label='RDS/A')
plot(keys(oil), values(oil), '-r', label='OIL')
legend(loc='upper right')

locs, _ = yticks()
yticks(locs, map(lambda x: "$%.2f" % x, locs))
locs, _ = xticks()
xticks(locs, map(lambda x: datetime.fromtimestamp(x).strftime('%Y/%m/%d'), locs))

figure()
title('Normalized graph of the relationship between stocks and commodities')

#plot(keys(aapl), normalize(values(aapl)), '--m', label='AAPL')
#plot(keys(bac), normalize(values(bac)), '--k', label='BAC')
plot(keys(xom), normalize(values(xom)), '-g', label='XOM')
#plot(keys(sd), normalize(values(sd)), '-b', label='SD')
#plot(keys(rdsa), normalize(values(rdsa)), '-c', label='RDS/A')
plot(keys(oil), normalize(values(oil)), '-r', label='OIL')
legend(loc='upper right')

locs, _ = yticks()
yticks(locs, map(lambda x: "%.3f" % x, locs))
locs, _ = xticks()
xticks(locs, map(lambda x: datetime.fromtimestamp(x).strftime('%Y/%m/%d'), locs))


"""

FFT.... failed.

figure()
title('Test graph of the relationship between stocks and commodities')
plot(rfft(normalize(values(aapl))), '--m', label='AAPL')
plot(rfft(normalize(values(bac))), '--k', label='BAC')
plot(rfft(normalize(values(xom))), '-g', label='XOM')
plot(rfft(normalize(values(sd))), '-b', label='SD')
plot(rfft(normalize(values(rdsa))), '-c', label='RDS/A')
plot(rfft(normalize(values(oil))), '-r', label='OIL')
legend(loc='upper right')

locs, _ = yticks()
yticks(locs, map(lambda x: "%.3f" % x, locs))
locs, _ = xticks()
xticks(locs, map(lambda x: x, locs))
"""

show()

