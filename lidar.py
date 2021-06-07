import random

import numpy as np
from math import *
import cv2
import matplotlib.pyplot as plt
import scipy as sc
import scipy.optimize as opt
from sklearn.linear_model import LinearRegression

lidarGeneratedData = []
pic = cv2.imread("whiteboard.png")

#lidarinput keeps distance to each point at each degree with step of 1 degree
def drawData(coordsArray):
    for i in range(len(coordsArray)):
        print('')
        #print("coordsArray for drawing is " +str(coordsArray))
        #print(coordsArray[i][0][0],coordsArray[i][1][0])
        #cv2.circle(pic, (int(coordsArray[i][0][0]*1000),int(coordsArray[i][1][0]*1000)), 3, (255,0,0), -1)
    #cv2.imshow("frame" , pic)
    #cv2.imwrite("result.png", pic)


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
print(f'limits are {twoPoints[5], twoPoints[6]}')
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
        if -90<=j<=90:
            j = radians(j)
            if (tan(j) != k):
                xIntersect = b / (tan(j) - k)
                if twoPoints[4] < xIntersect < twoPoints[5] and xIntersect>=0:
                    xIntersect = xIntersect
                    # intersectionsX.append([i,xIntersect])
                    intersectionsX.append([i, xIntersect])
                else:
                    intersectionsX.append([i, None])
                    # intersectionsX.append([i,'none'])
        if j< -90:
            j = radians(j)
            if (tan(j) != k):
                xIntersect = b / (tan(j) - k)
                if twoPoints[4] < xIntersect < twoPoints[5] and xIntersect < 0:
                    xIntersect = xIntersect
                    # intersectionsX.append([i,xIntersect])
                    intersectionsX.append([i, xIntersect])
                else:
                    intersectionsX.append([i, None])
                    # intersectionsX.append([i,'none'])
    return intersectionsX

intersectionsX = findIntersections()

#pointx = [3]
#print(f"Func value in point {pointx} is: {randFunc(pointx)}")
#print('')
#print(f'Intersection points of lidar with obstacles are: {intersectionsX}')
print(len(intersectionsX))

for unit in intersectionsX:
    alpha = unit[0]
    lengthX = unit[1]
    if lengthX is not None and sin(radians(alpha))!=0:
        lengthR = lengthX/sin(radians(alpha))
        lidarGeneratedData.append(round(lengthR,2))
    else:
        lidarGeneratedData.append(None)

print('')

def generateNoise(lidarGeneratedData):
    noisedData = np.array([])
    for datum in lidarGeneratedData:
        if datum is None:
            if np.random.uniform(0,100)<0.5:
                datum = np.random.uniform(0,20)
        else:
            datum += np.random.uniform(0,0.2)
        noisedData = np.append(noisedData, datum)

    #print(noisedData)

    return noisedData

noisedData  = generateNoise(lidarGeneratedData)


"""
THIS WAS THE INFORMATION GENERATION PART



FROM NOW ON, DATA ANALYSIS IS BEING IMPLEMENTED
"""
def data2coords(dist):
    overall = []
    xS = np.array([])
    yS = np.array([])
    c = 0
    #print('')
    #print(f'dist in data2coords is {dist}')

    for i in range (len(dist)):
        if dist[i] is not None:
            #print(f'dist[i] is {dist[i]}')
            xCoordinate = dist[i]*sin(radians(i))
            xS = np.append(xS, xCoordinate)
            #print(f'appended {xCoordinate} to xS: {xS}')
            yCoordinate = dist[i]*cos(radians(i))
            yS = np.append(yS, yCoordinate)
            overall.append([xCoordinate, yCoordinate])
    return  xS, yS
    #return overall

def data2coords4line (line):
    xS = np.array([])
    yS = np.array([])
    c = 0
    # print('')
    # print(f'dist in data2coords is {dist}')

    for point in line:
        xCoordinate = point[0] * sin(radians(point[1]))
        xS = np.append(xS, xCoordinate)
        # print(f'appended {xCoordinate} to xS: {xS}')
        yCoordinate = point[0] * cos(radians(point[1]))
        yS = np.append(yS, yCoordinate)
    return xS, yS

def data2coordsov(dist):
    overall = []
    xS = np.array([])
    yS = np.array([])
    c = 0
    #print('')
    #print(f'dist in data2coords is {dist}')

    for i in range (len(dist)):
        if dist[i] is not None:
            #print(f'dist[i] is {dist[i]}')
            xCoordinate = dist[i]*sin(radians(i))
            xS = np.append(xS, xCoordinate)
            #print(f'appended {xCoordinate} to xS: {xS}')
            yCoordinate = dist[i]*cos(radians(i))
            yS = np.append(yS, yCoordinate)
            overall.append([xCoordinate, yCoordinate])
    #return  xS, yS
    return overall


def LinesSplit(inputData):
    lines = []
    linesWithoutAngle = []
    lineNum = 0
    inputData = np.append(inputData, inputData[0])
    inputData = np.insert(inputData,0, inputData[-2])

    #print(f'inputData in linessplit is {inputData} after appending and inserting 2 basics')
    flag = 1
    for i in range(1, len(inputData)-1):
        if inputData[i] is not None:
            if inputData[i+1] is not None or inputData[i-1] is not None:
                if flag == 1:
                    lines.append([])
                    linesWithoutAngle.append([])
                    flag = 0
                lines[-1].append([inputData[i],i - 1])
                linesWithoutAngle[-1].append([inputData[i]])
                #print(f'appended {[inputData[i],i - 1]} to lines in linessplit')
                #print(f'now lines are {lines}')
            else:
                lineNum +=1
                flag = 1
    #if lines[0][0][1] == 0 and lines[-1][-1][1] == 359:
    #    for k in range(len(lines[0])):
    #        lines[-1].append(lines[0][k])
    #    lines.pop(0)

    return lines




def process_data(data):   #data is an array of length with each degree
    lines = LinesSplit(data) #lines are arrays in array thet give radius and angle
    print(f'data is {data}')

    outData = []


    for line in lines:
        print(f'line is: {line}')
        modelIntercepts = []
        modelCoefs = []

        X, Y = data2coords4line(line)
        #xS = np.array([])
        yS = Y
        xS = X.reshape(-1,1)
        #yS = np.array([])
        #lineNP = np.array(line)
        #drawData(data2coordsov(lineNP))
        #print(f'lineNP is given to data2coords as data. Its value is {lineNP}')
        #xS = np.append(xS, data2coords(lineNP)[0])
        #print(f'xS = {xS}')
        #print(f'xS length is {len(xS)}')
        #yS = np.append(yS, data2coords(lineNP)[1])
        #xS = np.array(xS).reshape(-1, 1)

        model = LinearRegression().fit(xS, yS)

        #print(f'intercept: {model.intercept_}')
        modelIntercepts.append(model.intercept_)
        #print(f'slope: {model.coef_}')
        modelCoefs.append(model.coef_[0])

        #print(xS)
        xSSorted = np.sort(xS, axis = 0)
        print(f'xSorted are {xSSorted}')
        xLowerLimit = xSSorted[-1][0]
        xHigherLimit = xSSorted[0][0]
        outData.append([modelIntercepts,modelCoefs, xLowerLimit, xHigherLimit])

    #print (f'modelIntercepts are {modelIntercepts}, modelCoefs are {modelCoefs}')
    #print('')
    print(f'outData is {outData}')
    return outData


def displayPoints(dataset):
    X, Y = data2coords(dataset)
    plt.scatter(X, Y)
    print(X)
    #print(X,Y, sep = "\n" )
    datanp = np.array(dataset)
    plt.scatter(datanp, range(360))
    plt.scatter(0,0)
    plt.show()

displayPoints(noisedData)
process_data(noisedData)
