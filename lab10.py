from cv2 import cv2
import tello
import time
import numpy as np
import math
from enum import Enum
from util import *
import matplotlib.pyplot as plt

class State(Enum):
    INIT = 1
    FLY_ACROSS = 2


def main():
    drone = tello.Tello('', 8889)
    time.sleep(10)
    f = cv2.FileStorage('calibration.xml', cv2.FILE_STORAGE_READ)

    cameraMatrix = f.getNode("intrinsic").mat()
    distCoeffs = f.getNode('distortion').mat()
    dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    parameters = cv2.aruco.DetectorParameters_create()

    intrinsic = cameraMatrix
    distortion = distCoeffs

    state = State.INIT
    line_state = 0


    while(True):
        frame = drone.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
        next_frame = frame



        next_frame = cv2.cvtColor(next_frame, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([110,50,50])
        upper_blue = np.array([130,255,255])

        mask = cv2.inRange(next_frame, lower_blue, upper_blue)
        res = cv2.bitwise_and(next_frame, next_frame, mask = mask)

        kernel_size = 5


        gray = cv2.cvtColor(next_frame, cv2.COLOR_BGR2GRAY)
        blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size), 0)
        edges_frame = cv2.Canny(blur_gray, 100, 200)
        dilation = cv2.dilate(edges_frame, (kernel_size, kernel_size), iterations=5)


        if len(markerCorners) > 0 and state == State.INIT:
            frame = cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIds)

            rvec, tvec, _objPoints = cv2.aruco.estimatePoseSingleMarkers(markerCorners, 15, intrinsic, distortion)
            cv2.putText(frame, str(tvec), (10, 40), cv2.FONT_HERSHEY_PLAIN,1, (0, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, str(rvec), (10, 400), cv2.FONT_HERSHEY_PLAIN,1, (0, 255, 255), 1, cv2.LINE_AA)

            idx = get_lowest_id(markerIds)
            id = markerIds[idx][0] 
            degree, distance, left_right, up_down = get_coloser(drone, tvec, rvec, 60, idx)
            cv2.putText(frame, str(degree), (10, 200), cv2.FONT_HERSHEY_PLAIN,1, (0, 255, 255), 1, cv2.LINE_AA)

            if tvec[0][0][2] < 70 and abs(degree - 90) < 10 and abs(left_right) < 20:
                state = State.FLY_ACROSS
                time.sleep(5)
                drone.move_right(40/100)
                

        x, y = pixelsum(dilation)
        x_var = np.std(x)
        y_var = np.std(y)
        print(x_var, y_var)


        

        if state == State.FLY_ACROSS:
            if line_state == 0:
                drone.move_right(20/100)
                if x_var > 2000 and y_var > 2000:
                    line_state = 1
                    time.sleep(5)
                    drone.move_up(40/100)
                    time.sleep(5)

            elif line_state == 1:
                drone.move_up(20/100)
                if x_var > 2000 and y_var > 2000:
                    line_state = 2
                    time.sleep(5)
                    drone.move_right(20/100)
                    time.sleep(5)

            elif line_state == 2:
                drone.move_right(20/100)
                if x_var > 2000 and y_var > 2000:
                    line_state = 3
                    time.sleep(5)
                    drone.move_up(40/100)
                    time.sleep(5)

            elif line_state == 3:
                drone.move_up(20/100)
                if x_var > 2000 and y_var > 2000:
                    line_state = 4
                    time.sleep(5)
                    drone.move_left(20/100)
                    time.sleep(5)

            elif line_state == 4:
                drone.move_left(20/100)
                if x_var > 2000 and y_var > 2000:
                    line_state = 5
                    time.sleep(5)
                    drone.move_down(40/100)
                    time.sleep(5)

            elif line_state == 5:
                drone.move_down(20/100)
                if x_var > 2000 and y_var > 2000:
                    line_state = 6
                    time.sleep(5)

            elif line_state == 6:
                drone.land()
                time.sleep(5)
        

            



        
        '''plt.plot(y)
        plt.plot(x)
        plt.show()'''



        cv2.imshow('frame', frame)
        cv2.imshow('dilation', dilation)
        key = cv2.waitKey(33)
        if key != -1:
            drone.keyboard(key)
            cv2.destroyAllWindows()


if __name__ == "__main__":
    main()