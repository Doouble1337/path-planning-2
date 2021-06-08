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
    def detect_object(image, bounds, approximation_coefficient):
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
            if stat[4]>1000:
                if stat[0]+stat[2]>right_side:
                    right_side = stat[0]+stat[2]
                if stat[1]<upper_side:
                    upper_side = stat[1]
                if stat[0]<left_side:
                    left_side = stat[0]
                if stat[1]+stat[3] > down_side:
                    down_side=stat[1]+stat[3]

        ret, mask = cv2.threshold(image[upper_side:down_side ,left_side:right_side, 0], 0, 255, cv2.THRESH_OTSU)

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_KCOS)

        hull = []
        for i in range(len(contours)):
            hull.append(cv2.convexHull(contours[i], False))


        for i in range(len(hull)):
            epsilon = approximation_coefficient * cv2.arcLength(hull[i], True)
            hull[i] = cv2.approxPolyDP(hull[i], epsilon, True)



        contours_image = np.zeros_like(image)
        cv2.drawContours(contours_image, contours, -1, (255, 255, 255), 1)
        cv2.drawContours(contours_image, hull, -1, (255, 255, 255), 1)

        return (contours_image, table_mask, hull)
