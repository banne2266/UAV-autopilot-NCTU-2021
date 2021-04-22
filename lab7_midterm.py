from cv2 import cv2
import tello
import time
import numpy as np
import math
from enum import Enum
from util import *

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
    land_find = 0
    
    while(True):
        frame = drone.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
        if len(markerCorners) > 0:
            frame = cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIds)

            rvec, tvec, _objPoints = cv2.aruco.estimatePoseSingleMarkers(markerCorners, 15, intrinsic, distortion)
            cv2.putText(frame, str(tvec), (10, 40), cv2.FONT_HERSHEY_PLAIN,1, (0, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, str(rvec), (10, 400), cv2.FONT_HERSHEY_PLAIN,1, (0, 255, 255), 1, cv2.LINE_AA)

            key = cv2.waitKey(33)
  

            if key != -1:
                drone.keyboard(key)
                cv2.destroyAllWindows()
            else:
                idx = get_lowest_id(markerIds)
                id = markerIds[idx][0] 
                print(tvec[idx][0][2])
                #print(id)
                if id == 0:      
                    degree, distance, left_right, up_down = get_coloser(drone, tvec, rvec, 90, idx)
                    cv2.putText(frame, str(degree), (10, 200), cv2.FONT_HERSHEY_PLAIN,1, (0, 255, 255), 1, cv2.LINE_AA)
                    
                elif id == 2: #fly higher
                    drone.move_up(50/100)

                elif id == 3: #auto pilot
                    if(state == State.INIT):#find id3
                        degree, distance, left_right, up_down = get_coloser(drone, tvec, rvec,70, idx)
                        cv2.putText(frame, str(degree), (10, 200), cv2.FONT_HERSHEY_PLAIN,1, (0, 255, 255), 1, cv2.LINE_AA)

                        if tvec[0][0][2] < 70 and abs(degree - 90) < 10 and abs(left_right) < 20:
                            state = State.FLY_ACROSS
                            
                    if(state == State.FLY_ACROSS):
                        time.sleep(5)
                        drone.move_down(80/100)
                        time.sleep(5)
                        drone.move_forward(150/100)
                        time.sleep(5)
                        drone.move_up(80/100)
                        state = State.INIT

                elif id == 4: #auto pilot
                    if(state == State.INIT):#find id4
                        degree, distance, left_right, up_down = get_coloser(drone, tvec, rvec, 70, idx)
                        cv2.putText(frame, str(degree), (10, 200), cv2.FONT_HERSHEY_PLAIN,1, (0, 255, 255), 1, cv2.LINE_AA)

                        if tvec[0][0][2] < 80 and abs(degree - 90) < 10 and abs(left_right) < 20:
                            state = State.FLY_ACROSS
                            
                    if(state == State.FLY_ACROSS):
                        time.sleep(5)
                        drone.move_up(80/100)
                        time.sleep(5)
                        drone.move_forward(150/100)
                        time.sleep(5)
                        drone.move_down(80/100)
                        state = State.INIT

                elif id == 5: #auto pilot
                    land_find = 1
                    if(state == State.INIT):#find id5
                        degree, distance, left_right, up_down = get_coloser(drone, tvec, rvec, 65, idx)
                        cv2.putText(frame, str(degree), (10, 200), cv2.FONT_HERSHEY_PLAIN,1, (0, 255, 255), 1, cv2.LINE_AA)

                        if abs(tvec[0][0][2]-60) < 20 and abs(degree - 90) < 10 and abs(left_right) < 15:
                            state = State.FLY_ACROSS
                            
                    if(state == State.FLY_ACROSS):
                        drone.land()
                        land_find = 0



        cv2.imshow('frame', frame)
        key = cv2.waitKey(100)
        if key != -1:
            drone.keyboard(key)
            cv2.destroyAllWindows()


if __name__ == "__main__":
    main()