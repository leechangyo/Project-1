import cv2
import numpy as np
background = None
background2 = None
background3 = None
accumulated_weight2 = 0.7
class calc_accum():
    # This background will be a global variable that we update through a few functions


    def calc_accum_avg(self,gray, accumulated_weight):

        '''
        Given a frame and a previous accumulated weight, computed the weighted average of the image passed in.
        '''

    # Grab the background
        global background


    # For first time, create the background from a copy of the frame.
        if background is None:
            # if the background is done meaning the very frist loop background is done here
            background  = gray.copy().astype("float")
            return None

            # compute weighted average, accumulate it and update the background
        cv2.accumulateWeighted(gray, background, accumulated_weight)

    def calc_accum_avg2(self,gray2, accumulated_weight3):
        '''
        Given a frame and a previous accumulated weight, computed the weighted average of the image passed in.
        '''

        # Grab the background
        global background2

        # For first time, create the background from a copy of the frame.
        if background2 is None:
            # if the background is done meaning the very frist loop background is done here
            background2 = gray2.copy().astype("float")
            return None


        # compute weighted average, accumulate it and update the background
        cv2.accumulateWeighted(gray2, background2, accumulated_weight2)

    def calc_accum_avg3(self,object_gray, accumulated_weight3):
        '''
        Given a frame and a previous accumulated weight, computed the weighted average of the image passed in.
        '''

        # Grab the background
        global background3

        # For first time, create the background from a copy of the frame.
        if background3 is None:
            # if the background is done meaning the very frist loop background is done here
            backgorund3  = object_gray.copy().astype("float")
            return None


            # compute weighted average, accumulate it and update the background
        cv2.accumulateWeighted(object_gray, backgorund3 , accumulated_weight3)
