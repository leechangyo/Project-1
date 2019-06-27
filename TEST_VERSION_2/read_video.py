import cv2
import numpy as np
import imutils
from scipy.spatial import distance as dist
import math
from motion_background import calc_accum
from segment import segment
from detect import detect
from centroid import centroid
from distance import distance
from multi_detect import multi_detect
from rotation import rotation
import sys
import rospy


class video():
    def __init__(self):
    # Manually set up our ROI for grabbing the hand.
    # Feel free to change these. I just chose the top right corner for filming.
        roi_top = 20
        roi_bottom = 140
        roi_right = 260
        roi_left = 380

    # ROI 2
        roi_top2 = 340
        roi_bottom2 = 460

        cam = cv2.VideoCapture(0)
        cam.set(3,640)
        cam.set(4,480)
    # Intialize a frame count
        num_frames = 0
    # background calc in real time
    # Start with a halfway point between 0 and 1 of accumulated weight
        accumulated_weight = 0.7
        accumulated_weight2 = 0.7
        accumulated_weight3 = 0.7
        background_calc = calc_accum()



        while True:
            # get the current frame
            ret, frame = cam.read()
            # flip the frame so that it is not the mirror view
            frame = cv2.flip(frame, 1)
            # clone the frame
            frame_copy = frame.copy()

            # object detection.
            height = frame_copy.shape[0]
            object_roi_top = height/2
            object_roi_bottom = 640
            object_detect = frame[object_roi_top:object_roi_bottom,:]
            object_gray = cv2.cvtColor(object_detect, cv2.COLOR_BGR2GRAY)
            object_gray = cv2.GaussianBlur(object_gray, (5, 5), 0)


        # ROI 1
        # Grab the ROI from the frame(1)
            roi = frame[roi_top:roi_bottom, roi_right:roi_left]
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        # Apply grayscale and blur to ROI
            gray = cv2.GaussianBlur(gray, (5, 5), 0)

        # ROI 2
            roi2 = frame[roi_top2:roi_bottom2, roi_right:roi_left]
            gray2 = cv2.cvtColor(roi2, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.GaussianBlur(gray2, (5, 5), 0)

        # For the first 60 frames we will calculate the average of the background.
            if num_frames < 60:
                background_calc.calc_accum_avg(gray, accumulated_weight)
                background_calc.calc_accum_avg2(gray2, accumulated_weight2)
                background_calc.calc_accum_avg3(object_gray, accumulated_weight3)
                if num_frames <= 59:
                    cv2.putText(frame_copy, "WAIT! GETTING BACKGROUND AVG.", (1, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
                    cv2.imshow("Vision",frame_copy)
            else:

                # shape detect upper
                upper_shape = segment(gray)
                if upper_shape is not None:
                    upper_thresh, upper_contour,upper_segment, upper_cnts = upper_shape
                    upper_shape_detect= detect(upper_contour)
                    # Apply hough transform on the image
                    (upper_cX,upper_cY,upper_c) = centroid(upper_cnts)


                    cv2.drawContours(frame_copy, [upper_segment+(roi_right,roi_top)], -1, (255,0,0),1)
                    cv2.circle(frame_copy, (upper_cX+roi_right, roi_top+upper_cY),7,(255,0,0),-1)
                    cv2.putText(frame_copy,"upper_shape : "+ str(upper_shape_detect),(1,440),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)

                    cv2.imshow("upper_threshold", upper_thresh)
                    # shape detect bottom
                bottom_shape = segment(gray2)
                if bottom_shape is not None:
                    bottom_thresh, bottom_contour,bottom_segment, bottom_cnts = bottom_shape
                    bottom_shape_detect= detect(bottom_contour)
                    (bottom_cX,bottom_cY,bottom_c) = centroid(bottom_cnts)

                    cv2.drawContours(frame_copy, [bottom_segment + (roi_right, roi_top2)], -1, (255,0,0),1)
                    cv2.putText(frame_copy,"bottom_shape : "+ str(bottom_shape_detect),(1,460),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
                    cv2.circle(frame_copy, (bottom_cX+roi_right, roi_top2+bottom_cY),7,(255,0,0),-1)
                    cv2.imshow("bottom_threshold", bottom_thresh)


                # distance
                upper_c=(upper_cX+roi_right, roi_top+upper_cY)
                bottom_c=(bottom_cX+roi_right, roi_top2+bottom_cY)
                roi_distance = distance(upper_c,bottom_c)
                cv2.putText(frame_copy,"ROI DISTANCE={} ".format(roi_distance),(1,400),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)

                if upper_shape_detect== "square" or "rectangle" and  bottom_shape_detect== "square" or "rectangle":
                    angles = rotation(bottom_c,upper_c)
                    cv2.putText(frame_copy,"difference ={}".format(angles),(1,420),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
                object_detect = segment(object_gray)
                if object_detect is not None:
                    object_thresh, object_contour,object_segment, object_cnts =  object_detect
                    multi_obejct_detect=multi_detect()
                    multi_obejct_detect.detect(frame_copy[object_roi_top:object_roi_bottom,:],object_contour)

    # Draw ROI Rectangle on frame copy
            cv2.rectangle(frame_copy, (roi_left, roi_top), (roi_right, roi_bottom), (0,0,255), 5)
            cv2.rectangle(frame_copy, (roi_left, roi_top2), (roi_right, roi_bottom2), (0,0,255),5)


    # increment the number of frames for tracking
            num_frames += 1
    #print(distance(upper_c,bottom_c))

    # Display the frame with segmented hand
            cv2.imshow("Vision", frame_copy)


    # Close windows with Esc
            k = cv2.waitKey(1) & 0xFF

            if k == 27:
                break
        cam.release()
        cv2.destroyAllWindows()


def main():
    video()
    rospy.init_node('image_converter', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("shutting down")
    

if __name__ == '__main__':
    try:
        main()
    except:
        print("error")
