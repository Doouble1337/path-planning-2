import numpy as np
import cv2


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


class ObjectDetector:

    @staticmethod
    def detect_object(image, bounds, approximation_coefficient, morphology_coefficient):
        lower, upper = bounds
        blur_kernel = (30, 30)
        blur = cv2.blur(image, blur_kernel)

        table_mask = cv2.inRange(blur, lower, upper)

        connect = cv2.connectedComponentsWithStats(table_mask, 4, cv2.CV_32S)
        right_side = 0
        down_side = 0
        upper_side = 1000000
        left_side = 1000000
        for stat in connect[2][1:]:
            if stat[4] > 1000:
                if stat[0] + stat[2] > right_side:
                    right_side = stat[0] + stat[2]
                if stat[1] < upper_side:
                    upper_side = stat[1]
                if stat[0] < left_side:
                    left_side = stat[0]
                if stat[1] + stat[3] > down_side:
                    down_side = stat[1] + stat[3]

        morph = cv2.morphologyEx(image, cv2.MORPH_OPEN,
                                 np.ones((morphology_coefficient, morphology_coefficient), np.uint8), iterations=1)

        ret, mask = cv2.threshold(morph[upper_side:down_side, left_side:right_side, 1], 0, 255, cv2.THRESH_OTSU)

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_KCOS)

        hull = []
        for i in range(len(contours)):
            hull.append(cv2.convexHull(contours[i], False))

        for i in range(len(hull)):
            epsilon = approximation_coefficient * cv2.arcLength(hull[i], True)
            hull[i] = cv2.approxPolyDP(hull[i], epsilon, True)

        contours_image = np.zeros_like(mask)
        cv2.drawContours(contours_image, contours, -1, (255, 255, 255), 1)
        hull_image = np.zeros_like(mask)
        cv2.drawContours(hull_image, hull, -1, (255, 255, 255), 1)

        return (table_mask, contours_image, hull_image, morph, hull)


def getCameraMatrix():
    with np.load('calib.npz') as X:
        camera_matrix, dist_coeff, _, _ = [X[i] for i in ('mtx', 'dist', 'rvecs', 'tvecs')]
    return camera_matrix, dist_coeff

def getArucoDict(markerSize=6, totalMarkers=250):
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    arucoDict = aruco.Dictionary_get(key)
    return arucoDict

camera_matrix, dist_coeff = getCameraMatrix()

from IPython.display import clear_output
from cv2 import aruco

cam1 = cv2.VideoCapture(0)

cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
cv2.namedWindow("sliders_frame", cv2.WINDOW_NORMAL)

lower_bound = np.array([0, 0, 0])
upper_bound = np.array([0, 0, 0])

cv2.createTrackbar('lower_red', 'sliders_frame', 0, 255, on_change)
cv2.createTrackbar('lower_green', 'sliders_frame', 0, 255, on_change)
cv2.createTrackbar('lower_blue', 'sliders_frame', 0, 255, on_change)

cv2.createTrackbar('upper_red', 'sliders_frame', 230, 255, on_change)
cv2.createTrackbar('upper_green', 'sliders_frame', 225, 255, on_change)
cv2.createTrackbar('upper_blue', 'sliders_frame', 215, 255, on_change)

ind = 1

while (True):
    _, frame = cam1.read()
    # frame = cv2.imread('test.png')
    # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    lower_bound[0] = cv2.getTrackbarPos('lower_red', 'sliders_frame')
    lower_bound[1] = cv2.getTrackbarPos('lower_green', 'sliders_frame')
    lower_bound[2] = cv2.getTrackbarPos('lower_blue', 'sliders_frame')

    upper_bound[0] = cv2.getTrackbarPos('upper_red', 'sliders_frame')
    upper_bound[1] = cv2.getTrackbarPos('upper_green', 'sliders_frame')
    upper_bound[2] = cv2.getTrackbarPos('upper_blue', 'sliders_frame')

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = getArucoDict()
    parameters = aruco.DetectorParameters_create()

    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    clear_output(wait=True)
    if not np.all(ids != None):
        print("NO MARKER")
        cv2.waitKey(1)
        continue
    else:
        print("FOUND MARKER")

    surface_mask, contours_frame, approx_contours_frame, morphed_frame, objects = ObjectDetector.detect_object(frame, (
    lower_bound, upper_bound), 0.01, 15)
    cv2.imshow("surface", surface_mask)
    cv2.imshow("frame", frame)
    cv2.imshow("contours", contours_frame)
    cv2.imshow("morph", morphed_frame)
    cv2.imshow("hull", approx_contours_frame)

    if (cv2.waitKey(33) == ord('z')):
        print("here")
        cv2.imwrite("img/frame_" + str(ind) + ".png", frame)
        cv2.imwrite("img/surface_mask_" + str(ind) + ".png", surface_mask)
        cv2.imwrite("img/contours_" + str(ind) + ".png", contours_frame)
        cv2.imwrite("img/morph_" + str(ind) + ".png", morphed_frame)
        cv2.imwrite("img/approx_contours_" + str(ind) + ".png", approx_contours_frame)
        ind += 1