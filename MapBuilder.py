import cv2
from cv2 import aruco
import numpy as np

class MapBuilder:

    @staticmethod
    def build_map(frame, objects, objectsHeight = 0, markerSize = 6, sizex = 500, sizey = 600, padding = 0.0):
        def getCameraMatrix():
            with np.load('calib.npz') as X:
                camera_matrix, dist_coeff, _, _ = [X[i] for i in ('mtx', 'dist', 'rvecs', 'tvecs')]
            return camera_matrix, dist_coeff

        def getArucoDict(markerSize, totalMarkers=250):
            key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
            arucoDict = aruco.Dictionary_get(key)
            return arucoDict

        camera_matrix, dist_coeff = getCameraMatrix()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        aruco_dict = getArucoDict(markerSize)
        parameters = aruco.DetectorParameters_create()

        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        if not np.all(ids != None):
            return None, None

        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners[0], 0.053, camera_matrix, dist_coeff)
        rmat = np.zeros(shape=(3, 3))
        cv2.Rodrigues(rvec, rmat)
        tvec = tvec.reshape((-1, 1))


        realCords = []

        left = np.matmul(np.linalg.inv(rmat), np.linalg.inv(camera_matrix))
        right = np.matmul(np.linalg.inv(rmat), tvec)


        mnx = 10000.
        mxx = -10000.
        mny = 10000.
        mxy = -10000.

        for object in objects:
            cords = []
            for point in object:
                p = np.array([[point[0][0]], [point[0][1]], [1]])
                c = (right[2][0] + objectsHeight) / np.matmul(left, p)[2][0]

                realp = (c * np.matmul(left, p)) - right
                cords.append(np.array([realp[0][0], realp[1][0]]))

                mnx = min(mnx, realp[0][0])
                mny = min(mny, realp[1][0])
                mxx = max(mxx, realp[0][0])
                mxy = max(mxy, realp[1][0])

            realCords.append(np.array(cords))
        realCords = np.array(realCords)

        #mnx = min(mnx, tvec[0][0])
        #mny = min(mny, tvec[1][0])
        #mxx = max(mxx, tvec[0][0])
        #mxy = max(mxy, tvec[1][0])

        scale = min(sizey / (mxy - mny + 2*padding), sizex / (mxx - mnx + 2*padding))

        res = np.zeros((sizex, sizey))
        st = np.array([mnx, mny])
        for object in realCords:
            contour = []
            for point in object:
                #print(point)
                x, y = scale * (point - st + np.array([padding, padding]))
                x = int(x)
                y = int(y)
                contour.append(np.array([x, y]))
            contour = np.array(contour)
            cv2.fillPoly(res, pts = [contour], color = (255, 255, 255))

        #xc, yc = scale * (np.array([tvec[0][0], tvec[1][0]]) - st + np.array([padding, padding]))
        #xc = int(xc)
        #yc = int(yc)
        #res = cv2.circle(res, np.array([yc, xc]), 5, (100, 100, 100), 2)

        return res, scale
