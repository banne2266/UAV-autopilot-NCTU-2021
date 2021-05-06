from cv2 import cv2
import tello
import time
import numpy as np

src = cv2.VideoCapture(0)
chase_count = 0
chase_image_list = []
chase_corner_list = []
objp = np.zeros((9*6, 3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

while(True):
    ret, frame = src.read()
    imageSize = (frame.shape[0], frame.shape[1])
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    ret, corner = cv2.findChessboardCorners(frame, (9,6), None)
    if ret == True:
        chase_count += 1
        cv2.cornerSubPix(frame, corner, (11,11), (-1,-1), criteria)
        chase_image_list.append(objp)
        chase_corner_list.append(corner)
        cv2.waitKey(500)
    
    if chase_count > 10:
        retval, cameraMatrix, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(chase_image_list,  chase_corner_list, imageSize, None, None)
        break

    cv2.imshow('frame', frame)
    key = cv2.waitKey(33)
    
f = cv2.FileStorage('my_calibration.xml', cv2.FILE_STORAGE_WRITE)
f.write("intrinsic", cameraMatrix)
f.write("distortion", distCoeffs)
f.release()