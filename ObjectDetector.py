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
    def detect_object(image, lower, upper):
        blur_kernel = (30, 30)
        blur = cv2.blur(image, blur_kernel)

        table_mask = cv2.inRange(blur, lower, upper)

        connect = cv2.connectedComponentsWithStats(table_mask, 4, cv2.CV_32S)
        max_length = 0
        max_height = 0
        min_height = 1000000
        min_length = 1000000
        for stat in connect[2][1:]:
            #if stat[4]>1000:
                if stat[0]+stat[2]>max_length:
                    max_length = stat[0]+stat[2]
                if stat[1]<min_height:
                    min_height = stat[1]
                if stat[0]<min_length:
                    min_length = stat[0]
                if stat[1]+stat[3] > max_height:
                    max_height=stat[1]+stat[3]
                print(min_length, max_length, min_height, max_height)

        table_mask = cv2.cvtColor(table_mask, cv2.COLOR_GRAY2RGB)
        cv2.rectangle(table_mask, (min_length, min_height), (max_length, max_height), (255, 0, 0), 1)


        ret, mask = cv2.threshold(image[min_height:max_height ,min_length:max_length, 0], 0, 255, cv2.THRESH_OTSU)

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours_image = np.zeros_like(image)
        cv2.drawContours(contours_image, contours, -1, (255, 255, 255), 1)

        return (contours_image)






get_available_cameras()

cam1 = cv2.VideoCapture(1)

cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
cv2.namedWindow("sliders_frame", cv2.WINDOW_NORMAL)

#cv2.resizeWindow("frame", (960, 720))

lower_bound = np.array([160, 100, 40])
upper_bound = np.array([190, 130, 60])

cv2.createTrackbar('lower_red', 'sliders_frame', 170, 255, on_change)
cv2.createTrackbar('lower_green', 'sliders_frame', 170, 255, on_change)
cv2.createTrackbar('lower_blue', 'sliders_frame', 170, 255, on_change)

cv2.createTrackbar('upper_red', 'sliders_frame', 255, 255, on_change)
cv2.createTrackbar('upper_green', 'sliders_frame', 255, 255, on_change)
cv2.createTrackbar('upper_blue', 'sliders_frame', 255, 255, on_change)



while (True):
    ret1, frame = cam1.read()

    cv2.waitKey(1)

    #frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    lower_bound[0] = cv2.getTrackbarPos('lower_red', 'sliders_frame')
    lower_bound[1] = cv2.getTrackbarPos('lower_green', 'sliders_frame')
    lower_bound[2] = cv2.getTrackbarPos('lower_blue', 'sliders_frame')

    upper_bound[0] = cv2.getTrackbarPos('upper_red', 'sliders_frame')
    upper_bound[1] = cv2.getTrackbarPos('upper_green', 'sliders_frame')
    upper_bound[2] = cv2.getTrackbarPos('upper_blue', 'sliders_frame')

    contours_frame = ObjectDetector.detect_object(frame, lower_bound, upper_bound)

    cv2.imshow("frame", frame)
    cv2.imshow("contours", contours_frame)


    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break

cam1.release()

cv2.destroyAllWindows()