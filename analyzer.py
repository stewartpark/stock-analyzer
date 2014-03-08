#!/usr/bin/env python

from scipy.stats import pearsonr, spearmanr
from scipy.signal import correlate
from pylab import show, plot, figure, title, xlabel, ylabel, legend, yticks, xticks
import numpy as np
from numpy import linspace, sin, cos, pi, array, diff, real, imag, cov, abs, sum, ones 
from numpy.fft import fft, ifft, rfft, irfft
import csv
import dateutil
from datetime import datetime

def smooth(x,win_len=5, window='hamming'):
    if x.ndim != 1:
        raise ValueError, 'smooth only accepts 1 dimension arrays'
    if x.size < win_len:
        raise ValueError, 'Input vector needs to be bigger than window size'
    if win_len<3:
        return x
    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"
    s=np.r_[x[win_len-1:0:-1],x,x[-1:-win_len:-1]]
    if window == 'flat': #moving average
        w=np.ones(win_len,'d')
    else:
        f = getattr(np, window)
        w=f(win_len)
    y=np.convolve(w/w.sum(),s,mode='valid')
    return y


def normalize(a):
    b = []
    for x in a:
        b.append((x - min(a)) / (max(a)-min(a)))
    return array(b) 

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
def sampledown(n, k):
    d = []
    for x in k:
        for y in range(len(n)):
            if n[y][0] >= x: 
                if abs(n[y][0] - x) <= (3600 * 24 * 3): # < +-3days
                    d.append([x, n[y][1]])
                    break
    return d

def jyp_algo(x,y,plot_name=None):
    y = sampledown(y, keys(x))
    X = array(values(x)[len(x)-len(y):])
    Y = array(values(y))

    #X = smooth(X)
    #Y = smooth(Y)

    X = normalize(X)
    Y = normalize(Y)

    X = diff(diff(X))
    Y = diff(diff(Y))


    o1 = correlate(X, X)
    o2 = correlate(X, Y)

    if plot_name != None:
        figure()
        title(plot_name)
        plot(o1, label='o1')
        plot(o2, label='o2')
        legend(loc='upper right')
    #return sum(abs(o1 - o2)) 
    return pearsonr(o1, o2)[0]




start_t = 1078444800 # When the stock market started.

oil = load_commodity('OIL')
oil = filter(lambda x: x[0] >= start_t, oil)

aapl = load_stock('AAPL')
bac = load_stock('BAC')
xom = load_stock('XOM')
sd = load_stock('SD')
rdsa = load_stock('RDS-A')
cvs = load_stock('CVS')
wag = load_stock('WAG')
cvx = load_stock('CVX')
met = load_stock('MET')

#print jyp_algo(aapl, sd)

"""
figure()
plot( normalize(values(oil)), label='OIL' )
plot( normalize(values(cvs)), label='CVS' )
plot( normalize(values(sd)), label='SD' )
legend(loc='upper right')
"""

"""
print cov([normalize(values(oil)), normalize(values(cvs))])
print cov([normalize(values(oil)), normalize(values(aapl))])
print cov([normalize(values(oil)), normalize(values(bac))])
print '----'
print cov([normalize(values(oil)), normalize(values(rdsa))])
print cov([normalize(values(oil)), normalize(values(sd))])
print cov([normalize(values(oil)), normalize(values(xom))])
"""
print 'Bank of America and Oil:',jyp_algo(oil, bac, plot_name='BAC')
print 'CVS Caremark and Oil:', jyp_algo(oil, cvs)
print 'Walgreen and Oil:', jyp_algo(oil, wag)
print 'Apple and Oil:', jyp_algo(oil, aapl)
print '---'
print 'Sandridge Energy and Oil:', jyp_algo(oil, sd)
print 'ExxonMobil and Oil:', jyp_algo(oil, xom)
print 'Shell and Oil:', jyp_algo(oil, rdsa)
print 'Chevron and Oil:', jyp_algo(oil, cvx)
"""
print '---'
print 'ExxonMobil and Shell:', jyp_algo(xom, rdsa)
print 'Bank of American and Apple:', jyp_algo(bac, aapl)
print 'CVS Caremark and Walgreen:', jyp_algo(cvs, wag)
print 'CVS Caremark and Apple:', jyp_algo(cvs, aapl)
"""


"""
figure()
title('Graph of the relationship between stocks and commodities')

plot(keys(aapl), values(aapl), '--m', label='AAPL')
plot(keys(bac), values(bac), '--k', label='BAC')
plot(keys(cvs), values(cvs), '--y', label='CVS')
plot(keys(wag), values(wag), '--', label='WAG')
plot(keys(xom), values(xom), '-g', label='XOM')
plot(keys(sd), values(sd), '-b', label='SD')
plot(keys(rdsa), values(rdsa), '-c', label='RDS/A')
plot(keys(oil), values(oil), '-r', label='OIL')
legend(loc='upper right')

locs, _ = yticks()
yticks(locs, map(lambda x: "$%.2f" % x, locs))
locs, _ = xticks()
xticks(locs, map(lambda x: datetime.fromtimestamp(x).strftime('%Y/%m/%d'), locs))
"""
"""
figure()
title('Normalized graph of the relationship between stocks and commodities')

#plot(keys(aapl), normalize(values(aapl)), '--m', label='AAPL')
#plot(keys(bac), normalize(values(bac)), '--k', label='BAC')
plot(keys(cvs), normalize(values(cvs)), '--y', label='CVS')
plot(keys(wag), normalize(values(wag)), '--', label='WAG')
#plot(keys(xom), normalize(values(xom)), '-g', label='XOM')
plot(keys(sd), normalize(values(sd)), '-b', label='SD')
#plot(keys(rdsa), normalize(values(rdsa)), '-c', label='RDS/A')
plot(keys(oil), normalize(values(oil)), '-r', label='OIL')
legend(loc='upper right')

locs, _ = yticks()
yticks(locs, map(lambda x: "%.3f" % x, locs))
locs, _ = xticks()
xticks(locs, map(lambda x: datetime.fromtimestamp(x).strftime('%Y/%m/%d'), locs))
"""
