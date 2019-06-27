import cv2
import numpy as np
import imutils
def centroid(cnts):
    for c in cnts:
        M = cv2.moments(c)
        if M["m00"] !=0:
            cX = int((M["m10"] / M["m00"]))
            cY = int((M["m01"] / M["m00"]))
        else:
            cX, cY = 0,0
        central_coordinate = cX, cY
        return (cX,cY,central_coordinate)
