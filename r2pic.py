import numpy as np
import cv2
from ObjectDetector import ObjectDetector
from MapBuilder import MapBuilder
from GUI import GUI, Param
from tkinter import *
import time

cam1 = cv2.VideoCapture(0)

lower_bound = np.array([0, 0, 0])
upper_bound = np.array([0, 0, 0])
detalization = 0
approximation_coef = 0.

def on_params_change(ind, val):
    val = int(val)
    if(ind <= Param.LOWER_BLUE):
        lower_bound[ind] = int(255 * val / 100)
    elif(ind <= Param.UPPER_BLUE):
        upper_bound[ind - Param.UPPER_RED] = int(255 * val / 100)
    elif(ind == Param.DETALIZATION):
        detalization = int(9 * val / 100) + 1
    elif(ind == Param.APPROXIMATION_COEF):
        approximation_coef = 0.1 * val / 100



gui = GUI(on_params_change)
while(True):
    _, frame = cam1.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    contours_frame, surface, objects = ObjectDetector.detect_object(frame, (lower_bound, upper_bound), approximation_coef)
    map, scale = MapBuilder.build_map(frame, objects)
    if(map is None):
        map = np.zeros(frame.shape, np.uint8)
    else:
        map = cv2.cvtColor(map, cv2.COLOR_GRAY2RGB)

    surface = cv2.cvtColor(surface, cv2.COLOR_GRAY2RGB)
    left = np.concatenate((frame, surface), axis = 1)
    right = np.concatenate((contours_frame, map), axis = 1)
    res = np.concatenate((left, right), axis = 0)
    #print(res.shape)

    gui.set_image(res)
    gui.root.update()
    time.sleep(0.01)

