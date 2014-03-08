#!/usr/bin/env python



import Tkinter as t 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from matplotlib.figure import Figure 
from matplotlib import dates
import os

import data 
import analyzer



def go_analyze():
    n1= comp1.get()
    n2= comp2.get()
 
    d1 = data.load_data(n1)
    d2 = data.load_data(n2)

    o,x,y,axis = analyzer.advcorr(d1, d2)
    d = analyzer.decide(o)

    fig.clear()
    ax = fig.add_subplot(111)
    ax.set_title('Normalized graph of the historial prices')
    
    p1,=ax.plot(axis,x)
    p2,=ax.plot(axis,y)
    ax.legend([p1,p2], [n1,n2])
    ax.text(0.01,0.98,'Correlation: %f (%s)' % (o, d), ha='left', va='center', transform=ax.transAxes) 
    canvas.show()

root = t.Tk()
root.title("Stock/Commodities Correlation Analyzer")
root.minsize(500,600)
entries = t.Frame(root)
entries.pack()


cp = t.Frame(root)
cp.pack(side = t.BOTTOM)

t.Label(cp, text="Programmed by JYP (jyp@nerds.kr)").pack(side=t.RIGHT)


body = t.Frame(root)
body.pack(side = t.BOTTOM)

fig = Figure() 

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.show()
canvas.get_tk_widget().pack(side='bottom', fill='both', expand=1)

t.Label(entries, text="Commodity").pack(side=t.LEFT)
comp1 = t.Entry(entries)
comp1.insert(0,"GOOG/NYSE_SD")
comp1.pack(side=t.LEFT)
t.Label(entries, text="Stock").pack(side=t.LEFT)
comp2 = t.Entry(entries)
comp2.insert(0,"OPEC/ORB")
comp2.pack(side=t.LEFT)

go = t.Button(entries,text="Go!",width=8,command=go_analyze)
go.pack(side=t.LEFT)

root.mainloop()
