import numpy as np
from math import *
import scipy as sc
import scipy.optimize as opt

lidarinput = [0]*360
lidarinput[0]=1
#lidarinput keeps distance to each point at each degree with step of 1 degree
print(lidarinput)

def generateLine():
    x0 = np.random.uniform(-5.0,5.0)
    y0 = np.random.uniform(-5.0,5.0)
    x1 = x0 + np.random.uniform(-10.0,10.0)
    y1 = y0 + np.random.uniform(-10.0, 10.0)
    xLowerLimit = np.random.uniform(-100.0,100.0)
    xUpperLimit = np.random.uniform(xLowerLimit, xLowerLimit+np.random.uniform(0, 100.0))
    twoPoints = [x0,y0,x1,y1,xLowerLimit,xUpperLimit] #x0,y0,x1,y1
    slope = (y1-y0)/(x1-x0)
    const = ((0 - x0) / (x1 - x0)) * (y1 - y0) + y0
    print(f"Generated points: {twoPoints}")
    print(f"Func eq is: {slope}x + {const}")
    print('')
    return twoPoints

twoPoints = generateLine()

def randFunc(x):
    twoPoints
    print(twoPoints[4] , x[0] , twoPoints[5])
    if twoPoints[4]<x[0]<twoPoints[5]:
        x0 = twoPoints[0]
        y0 = twoPoints[1]
        x1 = twoPoints[2]
        y1 = twoPoints[3]
        func = ((x[0] - x0) / (x1 - x0)) * (y1 - y0) + y0
        return func
    else:
        return "out of bounds"


def angleFunc(x):
    y = -x[0] + 90
    func  = np.tan(y)
    return (func)

def difFunc(x):
    func =  randFunc(x[0])-angleFunc(x[0])
    return func

def sqDifFunc(x):
    func = difFunc(x[0])**2
    return func

#xIntersection = opt.minimize(sqDifFunc, [0], options={'eps': 0.1})
#print(xIntersection)

def findIntersections():
    for i in range (360):
        j = -i + 90 #angle in normal coords

    return True


pointx = [12]
print(f"Func value in point {pointx} is: {randFunc(pointx)}")



