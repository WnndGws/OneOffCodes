# -*- coding: utf-8 -*-
"""
Created on Tue May 24 23:01:19 2016

@author: wynand
"""

import matplotlib.pyplot as pyplot
import numpy as np
import parser

coef = input("Please enter all coefficients of your equation (including zeros!) seperated by commas (eg. x^2 would be input as 1,0,0): ")
coef = list(map(float,coef.split(',')))
terms = len(coef)
equation = ""

params = 0
while params < terms:
    equation = equation + str("+" + str(coef[params]) + "*x**" + str(terms-params-1))
    params = params+1
    
def graph(formula,xmin,xmax):
    xTicks = (xmax-xmin)/200
    x = np.arange(xmin,xmax,xTicks)
    y = eval(equation)
    fig = pyplot.figure()
    ax = fig.add_subplot(111) 
    ax.plot(x,y)
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_smart_bounds(True)
    ax.spines['bottom'].set_smart_bounds(True)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.axhline(linewidth=2, color='blue')
    ax.axvline(linewidth=2, color='blue')    
    pyplot.show()
    
graph(equation,-100,100)

happy = 'no'
while happy == 'no':
    zoom = str(input('Would you like to zoom in further? (Yes/No): '))
    allowedZoom = ["Yes","Y","y","yes","YES","NO","no","No","N","n"]
    if zoom not in allowedZoom:
        print("Please enter only 'Yes' or 'No'")
        happy = 'no'
    elif ('y' or 'Y') in zoom:
        xmin = int(input('Enter x-min:' ))
        xmax = int(input('Enter x-max:' ))
        if xmin >= xmax:
            print ("Make sure that xmin is lower than xmax")
        else:            
            graph(equation,xmin,xmax)
        happy = 'no'
    else:
        happy = 'yes'        
        
r1estimate = float(input('Estimate the x-value of the 1st root: '))
code = parser.expr(equation).compile()

a=r1estimate-1
b=r1estimate+1
tol=0.001
roots = []

n = 1
nmax = 500
while nmax > n:    
    n = n+1    
    
    x = a
    fa = eval(code)
    if fa == 0:
        print(x)
        
    x = b
    fb = eval(code)
    if fb == 0:
        print(x)
        
    xmid = ((a+b)/2)
    x = xmid
    fxmid = eval(code)
    if (fxmid < tol):
        print("Trying x={0}....".format(x))
        print("y={0}".format(fxmid))
        print("x={0} is one of the roots!".format(x))
        roots.append(x)
        print("Roots = {0}".format(roots))
        n = n+100000
        break
    elif fxmid*fa > 0.0:
        b = xmid
    elif fxmid*fb > 0.0:
        a = xmid