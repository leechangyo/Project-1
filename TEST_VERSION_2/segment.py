import cv2
import numpy as np
import imutils
def segment(frame, threshold=25):

    np.uint8(frame)
    # We only need the threshold, so we will throw away the first item in the tuple with an underscore _
    _, thresholded = cv2.threshold(frame, threshold, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    contours, hierarchy= cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cnts= cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # If length of contours list is 0, then we didn't grab any contours!
    if len(contours) == 0:
        return None
    else:
        # Given the way we are using the program, the largest external contour should be the hand (largest by area)
        # This will be our segment
        segment = max(contours, key=cv2.contourArea)
    return (thresholded, contours, segment,cnts)
