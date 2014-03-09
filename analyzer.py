#!/usr/bin/env python

from scipy.stats import pearsonr, spearmanr
from scipy.signal import correlate
from pylab import show, plot, figure, title, xlabel, ylabel, legend, yticks, xticks
import numpy as np
from numpy import linspace, sin, cos, pi, array, diff, real, imag, cov, abs, sum, ones, corrcoef, gradient 
from numpy.fft import fft, ifft, rfft, irfft
import csv
import dateutil
from datetime import datetime

def normalize(a):
    b = []
    for x in a:
        b.append(float(x - min(a)) / float(max(a)-min(a)))
    return array(b) 

def keys(n):
    return map(lambda x: x[0], n)
def values(n):
    return map(lambda x: x[1], n)

def sampledown_monthly(n):
    """
        It changes the data set monthly.

    """
    d = []
    m = 0
    for x in n:
        mm = datetime.fromtimestamp(x[0]).month
        if m != mm:
            d.append(x)
            m = mm
    return d



def sampledown(n, k):
    """
        It eliminates data pairs that the other data set doesn't have.

    """
    d = []
    for x in k:
        for y in range(len(n)):
            if n[y][0] >= x: 
                if abs(n[y][0] - x) <= (3600 * 24 * 3): # < +-3days
                    d.append([x, n[y][1]])
                    break
    return d

def advcorr(x,y,name=None):
    """
        Gradient based correlation function  
            (aka a delicately crafted correlation algorithm through dumb parametric studies.)
    """

    # Decrease the samples since too much data might be noisy.
    x = sampledown_monthly(x)
    y = sampledown_monthly(y)
    y = sampledown(y, keys(x))
    x = sampledown(x, keys(y))
    axis = keys(x)


    # Trim the input array to avoid dumb dimension mismatched errors.
    X = array(values(x)[len(x)-len(y):])
    Y = array(values(y))

    # Normalize the prices.
    nX = normalize(X)
    nY = normalize(Y)

    # Calculate gradients
    dX = diff(nX)
    dY = diff(nY)

    # See the correlation
    o1 = correlate(dX, dX)
    o2 = correlate(dX, dY)
    o = pearsonr(o1, o2)

    return o[0], nX, nY, axis


def decide(o):
    m = ''
    
    if abs(o) >= 0.95:
        return 'Exact match'
    elif abs(o) >= 0.8:
        m+='very strongly '    
    elif abs(o) >= 0.6:
        m+='strongly '    
    elif abs(o) >= 0.4:
        m+='weakly '    
    elif abs(o) >= 0.2:
        m+='very weakly '    
    
    if o >= 0:
        m+='positive'
    else:
        m+='negative'


    return m.capitalize()


