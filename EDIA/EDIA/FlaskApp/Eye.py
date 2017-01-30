from FaceOrgan import FaceOrgan
import cv2
import numpy as np
import math

class Eye(FaceOrgan):
    """ This class represents an eye location in an image.
        the class finds the given eye pupil """
    def __init__(self, frame, eye, side):
        FaceOrgan.__init__(self, eye, "eye")
        self.side = side    #'r' for right eye and 'l' for left eye
        self.find_pupil(frame)

    # This function finds the eye pupil
    def find_pupil(self,frame):
        (x,y,w,h) = self.get_rect()
        center = (x+w/2,y+h/2)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # change to gray scale
        eye_rect = gray[y:y+h,x:x+w]                    # take the eye rectangle from the image
        equ = cv2.equalizeHist(eye_rect)        
        bin = np.zeros_like(equ)
        cv2.threshold(equ,  10, 255, cv2.THRESH_BINARY, bin)
        points = []         # list of all black points
        mid_points = []     # list of all black points located in the center of the rectangle
        for i in range(len(bin)):
            for j in range(len(bin[0])):
                if bin[i,j] == 0:
                    points.append((x+j,y+i))            # save black points from all eye-rectangle
                    if (h/3<i<2*h/3) and (w/3<j<2*w/3):
                        mid_points.append((x+j,y+i))    # save black points from the center of eye-rectangle
        points = np.array(points)
        mid_points = np.array(mid_points)
        if len(mid_points) == 0:
            return
        x = mid_points[:,0]
        y = mid_points[:,1]
        # find the median point
        x_med = int(np.median(x))
        y_med = int(np.median(y))

        x = points[:,0]
        y = points[:,1]
        x = abs(x - x_med) < w/5
        y = abs(y - y_med) < w/5
        # select the good points
        points = points[x == True]
        y = y[x==True]
        points = points[y==True]

        if len(points) > 0:
            (x,y),radius = cv2.minEnclosingCircle(points)
            self.center = (int(x),int(y))
            self.radius = int(radius)
          
    # This function returns the eye-pupil center and radius
    def get_pupil(self):
        try:
            return self.center,self.radius  # return pupil center
        except:
            return None                     # if we didnt found a pupil
        
    # This function draws the eye rectangle and pupil circle in the given frame        
    def mark_organ(self, frame, color):
        FaceOrgan.mark_organ(self,frame,color)
        try:            
            cv2.circle(frame,self.center,self.radius,(0,255,0),1)   #if we found a pupil
        except:
            return

# This function calculate the distance between two points
def calc_d(point1, point2):
    x = point1[0] - point2[0]
    y = point1[1] - point2[1]
    return math.hypot(x,y)