#!/usr/bin/env python

from scipy.stats import pearsonr 
from scipy.signal import correlate
from pylab import show, plot, figure, title, xlabel, ylabel, legend, yticks, xticks
from numpy import linspace, sin, cos, pi, array
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



aapl = load_stock('AAPL')
start_t = min(map(lambda x: x[0], aapl))

bac = load_stock('BAC')
bac = filter(lambda x: x[0] >= start_t, bac)

xom = load_stock('XOM')
xom = filter(lambda x: x[0] >= start_t, xom)

sd = load_stock('SD')
sd = filter(lambda x: x[0] >= start_t, sd)

rdsa = load_stock('RDS-A')
rdsa = filter(lambda x: x[0] >= start_t, rdsa)

oil = load_commodity('OIL')
oil = filter(lambda x: x[0] >= start_t, oil)

figure()
title('Graph of the relationship between stocks and commodities')

plot(map(lambda x: x[0], aapl), map(lambda x: x[1], aapl), '--m', label='AAPL')
plot(map(lambda x: x[0], bac), map(lambda x: x[1], bac), '--k', label='BAC')
plot(map(lambda x: x[0], xom), map(lambda x: x[1], xom), '-g', label='XOM')
plot(map(lambda x: x[0], sd), map(lambda x: x[1], sd), '-b', label='SD')
plot(map(lambda x: x[0], rdsa), map(lambda x: x[1], rdsa), '-c', label='RDS/A')
plot(map(lambda x: x[0], oil), map(lambda x: x[1], oil), '-r', label='OIL')
legend(loc='upper right')

locs, _ = yticks()
yticks(locs, map(lambda x: "$%.2f" % x, locs))
locs, _ = xticks()
xticks(locs, map(lambda x: datetime.fromtimestamp(x).strftime('%Y/%m/%d'), locs))
show()

figure()
title('Normalized graph of the relationship between stocks and commodities')

plot(map(lambda x: x[0], aapl), normalize(map(lambda x: x[1], aapl)), '--m', label='AAPL')
#plot(map(lambda x: x[0], bac), normalize(map(lambda x: x[1], bac)), '--k', label='BAC')
#plot(map(lambda x: x[0], xom), normalize(map(lambda x: x[1], xom)), '-g', label='XOM')
#plot(map(lambda x: x[0], sd), normalize(map(lambda x: x[1], sd)), '-b', label='SD')
plot(map(lambda x: x[0], rdsa), normalize(map(lambda x: x[1], rdsa)), '-c', label='RDS/A')
plot(map(lambda x: x[0], oil), normalize(map(lambda x: x[1], oil)), '-r', label='OIL')
legend(loc='upper right')

locs, _ = yticks()
yticks(locs, map(lambda x: "%.3f" % x, locs))
locs, _ = xticks()
xticks(locs, map(lambda x: datetime.fromtimestamp(x).strftime('%Y/%m/%d'), locs))
show()

