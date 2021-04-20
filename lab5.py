from cv2 import cv2
import tello
import time
import numpy as np

def main():
    drone = tello.Tello('', 8889)
    time.sleep(10)
    chase_count = 0
    chase_image_list = []
    chase_corner_list = []
    objp = np.zeros((9*6, 3), np.float32)
    objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    while(True):
        frame = drone.read()
        imageSize = (frame.shape[0], frame.shape[1])
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        ret, corner = cv2.findChessboardCorners(frame, (9,6), None)
        if ret == True:
            #print('detect')
            chase_count += 1
            cv2.cornerSubPix(frame, corner, (11,11), (-1,-1), criteria)
            chase_image_list.append(objp)
            chase_corner_list.append(corner)
            cv2.waitKey(500)
        
        if chase_count > 10:
            retval, cameraMatrix, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(chase_image_list,  chase_corner_list, imageSize, None, None)
            break

        cv2.imshow('frame', frame)
        cv2.waitKey(33)
        
        
    time.sleep(2)
    dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    parameters = cv2.aruco.DetectorParameters_create()

    intrinsic = cameraMatrix
    distortion = distCoeffs
    
    while(True):
        frame = drone.read()
        imageSize = (frame.shape[0], frame.shape[1])
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
        if len(markerCorners) > 0:
            frame = cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIds)

            rvec, tvec, _objPoints = cv2.aruco.estimatePoseSingleMarkers(markerCorners, 15, intrinsic, distortion)
            frame = cv2.aruco.drawAxis(frame, intrinsic, distortion, rvec, tvec, 0.1)

            text = 'x = ' + str(tvec[0]) + 'y = ' + str(tvec[1]) + 'z = ' + str(tvec[2])

            cv2.putText(frame, str(tvec), (10, 40), cv2.FONT_HERSHEY_PLAIN,1, (0, 255, 255), 1, cv2.LINE_AA)

        cv2.imshow('frame', frame)
        cv2.waitKey(33)

    if key!= -1:
        drone.keyboard(key)
        cv2.destroyAllWindows()
    


if __name__ == "__main__":
    main()