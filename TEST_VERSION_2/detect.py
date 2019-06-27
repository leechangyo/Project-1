import cv2
import numpy as np
def detect(c):
    box1=[]
    f_count=0
    select=0
    for cnt in c:
        shape = "unidenfied"
        peri = cv2.arcLength(cnt, True)
        # arcLength(,true): close line
        approx = cv2.approxPolyDP(cnt, 0.03 * peri, True)
        # approxpolydp help to find simple contour edge

        # if the shape is a triangle, it will have 3 vertices
        if len(approx) == 3:
            shape = "triangle"
            # if the shape has 4 vertices, it is either a square or
        elif len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "square" if ar >= 0.90 and ar <= 1.10 else "rectangle"
            # if the shape is a pentagon, it will have 5 vertices
        elif len(approx) == 5:
            shape = "pentagon"
            # otherwise, we assume the shape is a circle
        elif len(approx) == 6:
            shape = "hexagon"
        else:
            (x,y),radius =cv2.minEnclosingCircle(approx)
            if radius >= 10 and radius <=50:
                center = (int(x),int(y))
                shape = "circle"
            else:
                shape = "unienfied"
        # return the name of the shape
        return shape
