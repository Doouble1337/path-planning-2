import numpy as np
import cv2 as cv
import glob
import os

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((7*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)
# Arrays to store object points and image points from all the images
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane

# TODO import images from project directory
images = glob.glob('C:\chess\*.jpg')

for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (7,7),
                   cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE)
    # If desired number of corner are detected, we refine the pixel coordinates
    # and display them on the images of checker board
    if ret == True:
        objpoints.append(objp)
        # refining pixel coordinates for given 2d points
        corners2 = cv.cornerSubPix(gray,corners, (7,7), (-1,-1), criteria)
        imgpoints.append(corners)
        # Draw and display the corners
        cv.drawChessboardCorners(img, (7,7), corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(0)
cv.destroyAllWindows()

# Performing camera calibration by passing the value of known 3D points (objpoints)
# and corresponding pixel coordinates of the detected corners (imgpoints)

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
np.savez('../path-planning/calib.npz', mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)
# mtx = Intrinsic camera matrix
# dist = Lens distortion coefficients
# rvecs = Rotation specified as a 3×1 vector. The direction of the vector specifies the axis of rotation
# and the magnitude of the vector specifies the angle of rotation
# tvecs = 3×1 Translation vectors
