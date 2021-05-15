from cv2 import cv2
import tello
import time
import numpy as np
import math
from enum import Enum

def get_coloser(drone, tvec, rvec, go_distance, idx):
    up_down = tvec[idx][0][1] + 5
    distance = tvec[idx][0][2] - go_distance
    left_right = tvec[idx][0][0]

    dst, jaco = cv2.Rodrigues(rvec[idx][0])
    z_ = np.array([dst[0][2], dst[1][2], dst[2][2]])
    v = np.array([z_[0], 0, z_[2]])
    degree = math.atan2(z_[2], z_[0])
    degree = -degree * 180  / math.pi

    
    if up_down > 10:
        drone.move_down(up_down/100)
    elif up_down < -10:
        drone.move_up(-up_down/100)
    elif left_right > 15:
        drone.move_right(max(left_right*2/3, 20)/100)
    elif left_right < -15:
        drone.move_left(max(-left_right*2/3, 20)/100)

    elif degree > 100:
        drone.rotate_cw(10)
    elif degree < 80:
        drone.rotate_ccw(10)
    
    

    if distance > 0:
        print(drone.move_forward(max(distance*2/3, 20)/100))
    elif distance < -10:
        drone.move_backward(20/100)

    return degree, distance, left_right, up_down

def get_lowest_id(markerIds):
    idx = 0
    min_val = 9999
    for i in range(len(markerIds)):
        if markerIds[i][0] < min_val:
            idx = i
            min_val = markerIds[i][0]
    return idx



def pixelsum(frame):
    return np.sum(frame, axis = 0), np.sum(frame, axis = 1)