import numpy as np
import cv2
import time
from IPython.display import clear_output


def get_available_cameras(upper_bound=10, lower_bound=0):
    available = []

    for i in range(lower_bound, upper_bound):
        cap = cv2.VideoCapture(i)

        if (cap.isOpened()):
            available.append(i)

        cap.release()

    return available

def on_change(x):
    print(lower_bound, upper_bound)

def detect_obgect(image, lower_bound, upper_bound):
    ret, mask = cv2.threshold(image[:,:,0], 0, 255, cv2.THRESH_OTSU)

    #mask = cv2.inRange(image, lower_bound, upper_bound)

    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

    connect = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S)
    for stat in connect[2]:
        if stat[4] < 1000:
            # mask[stat[0]:stat[0]+stat[2], stat[1]:stat[1]+stat[3]] = [0, 0, 0]
            cv2.rectangle(image, (stat[0], stat[1]), (stat[0] + stat[2], stat[1] + stat[3]), (0, 255, 255), 1)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours_image = np.zeros_like(image)
    cv2.drawContours(contours_image, contours, -1, (255, 255, 255), 1)
    cv2.drawContours(image, contours, -1, (0, 255, 255), 1)

    return (contours_image, mask, image)






get_available_cameras()

cam1 = cv2.VideoCapture(0)

cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
cv2.namedWindow("sliders_frame", cv2.WINDOW_NORMAL)

cv2.resizeWindow("frame", (960, 720))

lower_bound = np.array([160, 100, 40])
upper_bound = np.array([190, 130, 60])

cv2.createTrackbar('lower_red', 'sliders_frame', 0, 255, on_change)
cv2.createTrackbar('lower_green', 'sliders_frame', 115, 255, on_change)
cv2.createTrackbar('lower_blue', 'sliders_frame', 0, 255, on_change)

cv2.createTrackbar('upper_red', 'sliders_frame', 30, 255, on_change)
cv2.createTrackbar('upper_green', 'sliders_frame', 255, 255, on_change)
cv2.createTrackbar('upper_blue', 'sliders_frame', 255, 255, on_change)

while (True):
    ret1, frame = cam1.read()

    cv2.waitKey(1)

    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    lower_bound[0] = cv2.getTrackbarPos('lower_red', 'sliders_frame')
    lower_bound[1] = cv2.getTrackbarPos('lower_green', 'sliders_frame')
    lower_bound[2] = cv2.getTrackbarPos('lower_blue', 'sliders_frame')

    upper_bound[0] = cv2.getTrackbarPos('upper_red', 'sliders_frame')
    upper_bound[1] = cv2.getTrackbarPos('upper_green', 'sliders_frame')
    upper_bound[2] = cv2.getTrackbarPos('upper_blue', 'sliders_frame')

    contours_frame, mask, frame = detect_obgect(frame, lower_bound, upper_bound)

    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("contours_frame", contours_frame)

    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break

cam1.release()

cv2.destroyAllWindows()