import numpy as np
import cv2
from ObjectDetector import ObjectDetector
from MapBuilder import MapBuilder

#get_available_cameras()

def on_change():
    pass

cam1 = cv2.VideoCapture(0)

cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
cv2.namedWindow("sliders_frame", cv2.WINDOW_NORMAL)

lower_bound = np.array([0, 0, 0])
upper_bound = np.array([0, 0, 0])

cv2.createTrackbar('lower_red', 'sliders_frame', 0, 255, on_change)
cv2.createTrackbar('lower_green', 'sliders_frame', 0, 255, on_change)
cv2.createTrackbar('lower_blue', 'sliders_frame', 0, 255, on_change)

cv2.createTrackbar('upper_red', 'sliders_frame', 255, 255, on_change)
cv2.createTrackbar('upper_green', 'sliders_frame', 255, 255, on_change)
cv2.createTrackbar('upper_blue', 'sliders_frame', 255, 255, on_change)



while (True):
    _, frame = cam1.read()
    #frame = cv2.imread('test.png')
    #frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    lower_bound[0] = cv2.getTrackbarPos('lower_red', 'sliders_frame')
    lower_bound[1] = cv2.getTrackbarPos('lower_green', 'sliders_frame')
    lower_bound[2] = cv2.getTrackbarPos('lower_blue', 'sliders_frame')

    upper_bound[0] = cv2.getTrackbarPos('upper_red', 'sliders_frame')
    upper_bound[1] = cv2.getTrackbarPos('upper_green', 'sliders_frame')
    upper_bound[2] = cv2.getTrackbarPos('upper_blue', 'sliders_frame')

    surface, contours_frame, objects = ObjectDetector.detect_object(frame, (lower_bound, upper_bound), 0.01)


    cv2.imshow("surface", surface)
    cv2.imshow("frame", frame)
    #cv2.imshow("contours", contours_frame)
    #for contour in contours_array:
    #    print(contour, end = ' end')

    map, scale = MapBuilder.build_map(frame, objects)

    if(map is not None):
        cv2.imshow("map", map)


    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break

cam1.release()

cv2.destroyAllWindows()