import numpy as np
import cv2
from ObjectDetector import ObjectDetector
from MapBuilder import MapBuilder
from GUI import GUI, Param
from tkinter import *
import time
from graphs import Graph

cam1 = cv2.VideoCapture('1234.mov')
# frame = cv2.imread("ggwp.png")
lower_bound = np.array([0, 0, 0])
upper_bound = np.array([230, 225, 215])
detalization = 10
approximation_coef = 0.0
morphology_coef = 11

def on_params_change(ind, val):
    global lower_bound, upper_bound, detalization, approximation_coef, morphology_coef
    if(ind <= Param.LOWER_BLUE):
        lower_bound[ind] = int(255 * val)
    elif(ind <= Param.UPPER_BLUE):
        upper_bound[ind - Param.UPPER_RED] = int(255 * val)
    elif(ind == Param.DETALIZATION):
        detalization = int(20 * val) + 10
    elif(ind == Param.APPROXIMATION_COEF):
        approximation_coef = 0.1 * val
    elif(ind == Param.MORPHOLOGY_COEF):
        morphology_coef = int(30 * val)




gui = GUI(on_params_change)

graph = Graph()

map_builder = MapBuilder()

files = ['frame_10'] #0,2,5,7,
filename = 'frame_11'

for filename in files:
    #_, frame = cam1.read()
    frame = cv2.imread('./' + filename + '.png')
    frame = frame[:420, :, :]
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    contours_frame, surface, objects = ObjectDetector.detect_object(frame, (lower_bound, upper_bound), approximation_coef, morphology_coef)
    map, scale = map_builder.build_map(frame, objects)
    if(map is None):
        gui.set_image(frame)
        gui.root.update()
        time.sleep(0.01)
        continue

    q = graph.gen_graph(map, detalization)

    imgp1 = (30, 190)
    imgp2 = (550, 200)

    p1 = map_builder.getPoint(imgp1, 0)
    p2 = map_builder.getPoint(imgp2, 0)

    frame = cv2.circle(frame, imgp1, 5, (255, 0, 0), 2)
    frame = cv2.circle(frame, imgp2, 5, (0, 0, 255), 2)

    #print(map_builder.getPointBack(p2))

    mp = np.zeros(frame.shape, np.uint8)

    try:
        t1 = time.time()
        path, mp = graph.search_path_dijkstra([p1[1], p1[0], 1], [p2[1], p2[0], 1])

       # print(time.time() - t1)

        path_on_img = []
        print(path)
        for point in path:
            imgpoint = map_builder.getPointBack(point)
            path_on_img.append(imgpoint)
        print(path_on_img)
       # print(frame.shape)

        for i in range(1, len(path_on_img)):
            cv2.line(frame, (path_on_img[i - 1][0], path_on_img[i - 1][1]), (path_on_img[i][0], path_on_img[i][1]), (0, 255, 0), 3)

    except:
        print("no path")

    #print(path)
    map = cv2.cvtColor(map, cv2.COLOR_GRAY2RGB)

   # print(p1, p2)
    map = cv2.circle(map, (p1[0], p1[1]), 5, (255, 0, 0), 2)
    map = cv2.circle(map, (p2[0], p2[1]), 5, (0, 0, 255), 2)

    q = cv2.circle(q, (p1[0], p1[1]), 5, (255, 0, 0), 2)
    q = cv2.circle(q, (p2[0], p2[1]), 5, (0, 0, 255), 2)


    map = np.flip(mp, axis = 0)
    q = np.flip(mp, axis = 0)
    surface = cv2.cvtColor(surface, cv2.COLOR_GRAY2RGB)
    left = np.concatenate((frame, contours_frame), axis = 1)
    right = np.concatenate((map, q), axis = 1)
    res = np.concatenate((left, right), axis = 0)

    #cv2.imshow('tk', frame)
    #print(frame.shape)
    #time.sleep(0.01)
    cv2.imwrite(filename + '-initial_picture.png', frame)
    #break
    cv2.imwrite(filename + '-contours.png', contours_frame)
    cv2.imwrite(filename + '-pic2r.png', q)
    cv2.imwrite(filename + '-map.png', map)


