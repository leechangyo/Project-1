import cv2
import numpy as np

class multi_detect():

    def setLabel(self,image, str, contour):
        (text_width, text_height), baseline = cv2.getTextSize(str, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 1)
        x,y,width,height = cv2.boundingRect(contour)
        pt_x = x+int((width-text_width)/2)
        pt_y = y+int((height + text_height)/2)
        cv2.rectangle(image, (pt_x, pt_y+baseline), (pt_x+text_width, pt_y-text_height), (200,200,200), cv2.FILLED)
        cv2.putText(image, str, (pt_x, pt_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 1, 8)

    def detect(self, image, object_contour):
        for cnt in object_contour:
            size = len(cnt)
            epsilon = 0.04 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            size = len(approx)
            area = cv2.contourArea(cnt)
            if area >= 500 and area <=4000:
                cv2.line(image, tuple(approx[0][0]), tuple(approx[size-1][0]), (0, 255, 0), 3)
                for k in range(size-1):
                    cv2.line(image, tuple(approx[k][0]), tuple(approx[k+1][0]), (0, 255, 0), 3)
                    if cv2.isContourConvex(approx):
                        if size == 3:
                            self.setLabel(image, "triangle", cnt)
                        elif size == 4:
                            self.setLabel(image, "rectangle", cnt)
                        elif size == 5:
                            self.setLabel(image, "pentagon", cnt)
                        elif size == 6:
                            self.setLabel(image, "hextagon", cnt)
                        else:
                            (x,y),radius =cv2.minEnclosingCircle(approx)
                            if radius >= 10 and radius <=50:
                                self.setLabel(image, "Circle",cnt)
                            else:
                                continue
