from cv2 import cv2
import tello
import time
import numpy as np
import dlib



src = cv2.VideoCapture(0)

f = cv2.FileStorage('calibration.xml', cv2.FILE_STORAGE_READ)
cameraMatrix = f.getNode("intrinsic").mat()
distCoeffs = f.getNode('distortion').mat()

detector = dlib.get_frontal_face_detector()

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


while(True):
    ret, frame = src.read()
    orig_frame = frame.copy()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    rects, weights = hog.detectMultiScale(frame, useMeanshiftGrouping = False)
    for rect in rects:
        orig_frame = cv2.rectangle(orig_frame, (rect[0], rect[1]), (rect[2], rect[3]), (0,255,255), 2)
        corners2 = np.array([[rect[0], rect[1]], [rect[2], rect[3]], [rect[0], rect[3]], [rect[2], rect[1]]], dtype=np.double)
        #右上 左下 右下 左上
        #print(corners2)       
        h = 180
        w = 180 / (rect[3] - rect[1]) * (rect[0] - rect[2])
        objp = np.array([[0,0,0] , [w,h,0], [0,h,0], [w,0,0]], dtype=np.double)
        retval, rvec, tvec = cv2.solvePnP(objp, corners2, cameraMatrix, distCoeffs)
        print(tvec)

        cv2.putText(orig_frame, "person: "+str(tvec[2][0]), (rect[0], rect[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 1, cv2.LINE_AA)


    face_rects = detector(frame, 0)
    for i, d in enumerate(face_rects):
        x1 = d.left()
        y1 = d.top()
        x2 = d.right()
        y2 = d.bottom()
        orig_frame = cv2.rectangle(orig_frame, (x1, y1), (x2, y2), (0,255,0), 2)

        objp = np.array([[0,0,0] , [16,16,0], [0,16,0], [16,0,0]], dtype=np.double)
        corners2 = np.array([[x1, y1], [x2, y2], [x1, y2], [x2, y1]], dtype=np.double)
        retval, rvec, tvec = cv2.solvePnP(objp, corners2, cameraMatrix, distCoeffs)
        #print(tvec)

        cv2.putText(orig_frame, "face: "+str(tvec[2][0]), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 1, cv2.LINE_AA)

    cv2.imshow('frame', orig_frame)
    cv2.waitKey(33)