import numpy as np
from math import *
import scipy as sc
import scipy.optimize as opt

lidarGeneratedData = []

#lidarinput keeps distance to each point at each degree with step of 1 degree

def generateLine():
    print('generated random line')
    x0 = np.random.uniform(-5.0,5.0)
    y0 = np.random.uniform(-5.0,5.0)
    x1 = x0 + np.random.uniform(-10.0,10.0)
    y1 = y0 + np.random.uniform(-10.0, 10.0)
    xLowerLimit = np.random.uniform(-1.0,1.0)
    xUpperLimit = np.random.uniform(xLowerLimit, xLowerLimit+np.random.uniform(0, 50.0))
    twoPoints = [x0,y0,x1,y1,xLowerLimit,xUpperLimit] #x0,y0,x1,y1
    slope = (y1-y0)/(x1-x0)
    const = ((0 - x0) / (x1 - x0)) * (y1 - y0) + y0
    print(f'slope is {slope}')
    print(f'const is {const}')
    twoPoints.append(slope)
    twoPoints.append(const)
    #print(f"Generated points: {twoPoints}")
    #print(f"Func eq is: {slope}x + {const}")
    #print('')
    return twoPoints

twoPoints = generateLine()
print(f'twoPoints is {twoPoints}')
#print(twoPoints)

#def randFunc(x):
#    print(twoPoints[4] , x[0] , twoPoints[5])
#    if twoPoints[4]<x[0]<twoPoints[5]:
#        x0 = twoPoints[0]
#        y0 = twoPoints[1]
#        x1 = twoPoints[2]
#        y1 = twoPoints[3]
#        func = ((x[0] - x0) / (x1 - x0)) * (y1 - y0) + y0
#        return func
#    else:
#        return "out of bounds"
#
#
#def angleFunc(alpha, x):
#    y = -alpha[0] + 90
#    func  = np.tan(y)*x
#    return (func)
#
#def difFunc(alpha, x):
#    func =  randFunc(x[0])-angleFunc(alpha, x[0])
#    return func
#
#def sqDifFunc(alpha, x):
#    func = difFunc(alpha, x[0])**2
#    return func
#
#xIntersection = opt.minimize(sqDifFunc, [0], options={'eps': 0.1})
#print(xIntersection)

def findIntersections():
    intersectionsX = []
    b = twoPoints[7]
    k = twoPoints[6]
    print(f'b is {b}')
    print(f'k is {k}')
    for i in range (360):
        j = -i + 90 #angle in normal coords
        j = radians(j)
        if (tan(j)!=k):
            xIntersect = b/(tan(j)-k)
            if twoPoints[4]<xIntersect<twoPoints[5]:
                xIntersect = round(xIntersect, 2)
                #intersectionsX.append([i,xIntersect])
                intersectionsX.append([i,xIntersect])
            else:
                intersectionsX.append([i,'none'])
                #intersectionsX.append([i,'none'])
    return intersectionsX

intersectionsX = findIntersections()

#pointx = [3]
#print(f"Func value in point {pointx} is: {randFunc(pointx)}")
print('')
print(f'Intersection points of lidar with obstacles are: {intersectionsX}')
print(len(intersectionsX))

for unit in intersectionsX:
    alpha = unit[0]
    lengthX = unit[1]
    if lengthX!='none':
        lengthR = lengthX/sin(radians(alpha))
        lidarGeneratedData.append(round(lengthR,2))
    else:
        lidarGeneratedData.append('none')

print('')
print(f'lidarGeneratedData array: {lidarGeneratedData}')