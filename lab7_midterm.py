from cv2 import cv2
import tello
import time
import numpy as np
import math
from enum import Enum

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
    
    while(True):
        frame = drone.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
        if len(markerCorners) > 0:
            frame = cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIds)

            rvec, tvec, _objPoints = cv2.aruco.estimatePoseSingleMarkers(markerCorners, 15, intrinsic, distortion)
            #frame = cv2.aruco.drawAxis(frame, intrinsic, distortion, rvec, tvec, 0.1)

            #text = 'x = ' + str(tvec[0][0][0]) + 'y = ' + str(tvec[0][0][1]) + 'z = ' + str(tvec[0][0][2])

            cv2.putText(frame, str(tvec), (10, 40), cv2.FONT_HERSHEY_PLAIN,1, (0, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, str(rvec), (10, 400), cv2.FONT_HERSHEY_PLAIN,1, (0, 255, 255), 1, cv2.LINE_AA)

            key = cv2.waitKey(33)
  

            if key != -1:
                drone.keyboard(key)
                cv2.destroyAllWindows()
            else:
                id = markerIds[0][0]

                if id == 0:      
                    up_down = tvec[0][0][1] - 15
                    distance = tvec[0][0][2] - 50
                    left_right = tvec[0][0][0]

                    dst, jaco = cv2.Rodrigues(rvec[0][0])
                    z_ = np.array([dst[0][2], dst[1][2], dst[2][2]])
                    v = np.array([z_[0], 0, z_[2]])
                    degree = math.atan2(z_[2], z_[0])
                    degree = -degree * 180  / math.pi

                    if left_right > 15:
                        drone.move_right(20/100)
                    elif left_right < -15:
                        drone.move_left(20/100)

                    elif degree > 100:
                        drone.rotate_cw(10)
                    elif degree < 80:
                        drone.rotate_ccw(10)
                    
                    elif up_down > 10:
                        drone.move_down(20/100)
                    elif up_down < -10:
                        drone.move_up(20/100)
                    
                    elif distance > 0:
                        print(drone.move_forward(max(distance/2, 20)/100))
                    elif distance < 0:
                        drone.move_backward(distance/100)

                    
                    cv2.putText(frame, str(degree), (10, 200), cv2.FONT_HERSHEY_PLAIN,1, (0, 255, 255), 1, cv2.LINE_AA)


                elif id == 3: #auto pilot
                    if(state == State.INIT):#find id4
                        up_down = tvec[0][0][1] + 5
                        distance = tvec[0][0][2] - 70
                        left_right = tvec[0][0][0]

                        dst, jaco = cv2.Rodrigues(rvec[0][0])
                        z_ = np.array([dst[0][2], dst[1][2], dst[2][2]])
                        v = np.array([z_[0], 0, z_[2]])
                        degree = math.atan2(z_[2], z_[0])
                        degree = -degree * 180  / math.pi

                        if left_right > 15:
                            drone.move_right(20/100)
                        elif left_right < -15:
                            drone.move_left(20/100)

                        elif degree > 100:
                            drone.rotate_cw(10)
                        elif degree < 80:
                            drone.rotate_ccw(10)
                        
                        elif up_down > 10:
                            drone.move_down(20/100)
                        elif up_down < -10:
                            drone.move_up(20/100)
                        
                        elif distance > 0:
                            print(drone.move_forward(max(distance/2, 20)/100))
                        elif distance < 0:
                            drone.move_backward(25/100)

                        
                        cv2.putText(frame, str(degree), (10, 200), cv2.FONT_HERSHEY_PLAIN,1, (0, 255, 255), 1, cv2.LINE_AA)

                      

                        if tvec[0][0][2] < 70 and abs(degree - 90) < 10 and abs(left_right) < 20:
                            state = State.FLY_ACROSS
                            
                    if(state == State.FLY_ACROSS):
                        time.sleep(4)
                        drone.move_down(80/100)
                        time.sleep(4)
                        drone.move_forward(150/100)
                        time.sleep(4)
                        drone.move_up(80/100)
                        state = State.INIT
                        
                        



                elif id == 4: #auto pilot
                    if(state == State.INIT):#find id4
                        up_down = tvec[0][0][1] - 15
                        distance = tvec[0][0][2] - 80
                        left_right = tvec[0][0][0]

                        dst, jaco = cv2.Rodrigues(rvec[0][0])
                        z_ = np.array([dst[0][2], dst[1][2], dst[2][2]])
                        v = np.array([z_[0], 0, z_[2]])
                        degree = math.atan2(z_[2], z_[0])
                        degree = -degree * 180  / math.pi

                        if left_right > 15:
                            drone.move_right(20/100)
                        elif left_right < -15:
                            drone.move_left(20/100)

                        elif degree > 105:
                            drone.rotate_cw(10)
                        elif degree < 75:
                            drone.rotate_ccw(10)
                        
                        elif up_down > 10:
                            drone.move_down(20/100)
                        elif up_down < -10:
                            drone.move_up(20/100)
                        
                        elif distance > 0:
                            print(drone.move_forward(max(distance/2, 20) / 100))
                        elif distance < 0:
                            drone.move_backward(25/100)

                        
                        cv2.putText(frame, str(degree), (10, 200), cv2.FONT_HERSHEY_PLAIN,1, (0, 255, 255), 1, cv2.LINE_AA)

                      

                        if tvec[0][0][2] < 80 and abs(degree - 90) < 10 and abs(left_right) < 20:
                            state = State.FLY_ACROSS
                            
                    if(state == State.FLY_ACROSS):
                        time.sleep(4)
                        drone.move_up(80/100)
                        time.sleep(4)
                        drone.move_forward(150/100)
                        time.sleep(4)
                        drone.move_down(80/100)
                        state = State.INIT

                elif id == 5: #auto pilot
                    if(state == State.INIT):#find id4
                        up_down = tvec[0][0][1] - 15
                        distance = tvec[0][0][2] - 70
                        left_right = tvec[0][0][0]

                        dst, jaco = cv2.Rodrigues(rvec[0][0])
                        z_ = np.array([dst[0][2], dst[1][2], dst[2][2]])
                        v = np.array([z_[0], 0, z_[2]])
                        degree = math.atan2(z_[2], z_[0])
                        degree = -degree * 180  / math.pi

                        if left_right > 10:
                            drone.move_right(20/100)
                        elif left_right < -10:
                            drone.move_left(20/100)

                        elif degree > 105:
                            drone.rotate_cw(10)
                        elif degree < 75:
                            drone.rotate_ccw(10)
                        
                        elif up_down > 10:
                            drone.move_down(20/100)
                        elif up_down < -10:
                            drone.move_up(20/100)
                        
                        elif distance > 10:
                            print(drone.move_forward(max(distance/2, 20) / 100))
                        elif distance < -10:
                            drone.move_backward(20/100)

                        
                        cv2.putText(frame, str(degree), (10, 200), cv2.FONT_HERSHEY_PLAIN,1, (0, 255, 255), 1, cv2.LINE_AA)

                      

                        if abs(tvec[0][0][2]-60) < 20 and abs(degree - 90) < 10 and abs(left_right) < 20:
                            state = State.FLY_ACROSS
                            
                    if(state == State.FLY_ACROSS):
                        time.sleep(4)
                        drone.land()

                        


                

        cv2.imshow('frame', frame)

        key = cv2.waitKey(100)
        if key != -1:
            drone.keyboard(key)
            cv2.destroyAllWindows()


if __name__ == "__main__":
    main()