import numpy as np
from CascadeDictionary import d
from Face import Face
from Face import calc_d
import cv2
import time
import math

class ImageAnalizer(object):
    """ This class receives a frame and previous frame and search
        faces in the frame using cascade classifiers an optical flow"""
    def __init__(self, frame, prev_frame, prev_faces, frame_num):
        self.frame = frame
        self.frame_num = frame_num
        self.faces = []
        # search face each 4'th frame or if there is no previous face to search with optical-flow
        if frame_num%4==0 or prev_faces[0] == None:
            self.face_detection(prev_faces)
            if len(self.faces) == 0 and prev_faces[0] != None:
                self.calc_optic_flow(prev_frame, prev_faces)
        else:
            if prev_faces[0] != None:
                self.calc_optic_flow(prev_frame, prev_faces)
            if len(self.faces) == 0:
                self.face_detection(prev_faces)

    # This function detect frontal/profile-faces in a given image
    def face_detection(self, prev_faces):
        # find faces
        print(d.items())
        #######################
        face_cascade = cv2.CascadeClassifier('C:\Users\Katia\Anaconda3\pkgs\opencv-3.1.0-np111py35_1\Library\etc\haarcascades\haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(self.frame, 1.5, 2)  
        p_faces =face_cascade.detectMultiScale(self.frame, 1.85, 2)
        if len(faces) == 0:
            faces = p_faces
        elif len(p_faces) != 0:
            faces = np.concatenate((faces, p_faces), 0)

        # choose the face with most face-organs
        for i,face in enumerate(faces):   
            x,y,w,h = face.ravel()         
            face_object = Face(face, self.frame, prev_faces,(255,0,0))
            if face_object.organs_counter > 0:
                if not self.is_face_exists(face):
                    self.faces.append(face_object)
                else:
                    face1,j = self.search_face(face_object)
                    if face_object.organs_counter > face1.organs_counter:
                        self.faces[j] = face_object

    # check if the face exist in the faces list 
    def is_face_exists(self,face1):
        x,y,w,h = face1.ravel()
        face1_center = (x+w/2, y+h/2)
        max_distance = h
        for face2 in self.faces:
            face2_center = face2.get_center()
            max_distance = max(max_distance,h)
            distance = calc_d(face1_center,face2_center)
            if distance < max_distance:
                return True
        return False
    
    # calculate the optical flow of the face between curent frame and previous frame
    def calc_optic_flow(self, prev_frame, prev_faces):
        #new_faces = []
        #cv2.imshow("ff",prev_frame)
        #for face in prev_faces:
        points = self.get_points(prev_faces[0])
        new_face = (optic_flow(prev_frame, self.frame, points))
        #for face in new_faces:
        face_object = Face(new_face, self.frame, prev_faces,(255,0,0))

        # check if face exists and choose the face with most organs
        if face_object.organs_counter > 0:
            face1,i = self.search_face(face_object)
            if face1 == None:
                self.faces.append(face_object)
            elif face_object.organs_counter > face1.organs_counter:
                self.faces[i] = face_object
    
    # search face to check if the face exists and choose the better one
    def search_face(self, face_object):
        for i,face in enumerate(self.faces):
            dx = max(face.w, face_object.w)
            dy = max(face.h, face_object.h)
            d = max(dx,dy)/2
            if calc_d(face.get_center(), face_object.get_center()) < d:
                return face,i
        return None,-1
    
    # crate list-of-points to search with optical flow
    def get_points(self, face):
        x,y,w,h = face.get_rect()
        rect = [[[x+1,y+1]],[[x+w-1,y+1]],
                [[x+1,y+h-1]],[[x+w-1,y+h-1]],
                [[x+w/2,y+1]],[[x+w-1,y+h/2]],
                [[x+w/2,y+h-1]],[[x+1,y+h/2]]]
        return rect

    # draw face and face organs in the given image
    def mark_faces(self,img):
        for face in self.faces:
            face.mark_face(img, (255,0,0))  

# The function calculate the optical flow of a given list of points
def optic_flow(prev_frame, frame, points): 
    height = len(frame)
    width = len(frame[0])     
    points = np.array(points, dtype='float32')    

    # parameters for lucas kanade optical flow
    lk_params = dict( winSize  = (15,15), maxLevel = 2,
                      criteria = (cv2.TERM_CRITERIA_EPS |
                                  cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    # calculate optical flow
    new_points, st, err = cv2.calcOpticalFlowPyrLK(prev_frame, frame,
                                                   points, None, **lk_params)
    # select good points
    new_points = np.concatenate((new_points[st==1],points[st==0]),0)
    new_points= new_points.tolist()
    p=[]
    for point in new_points:
        p.append([point])
    new_p = points.tolist()
    p =np.array(p,dtype='float32')
    for i,point in enumerate(new_points):
        if i < len(new_p):
            x1 = int(point[0])
            x2 = int(new_p[i][0][0])
            y1 = int(point[1])
            y2 = int(new_p[i][0][1])
    x,y,w,h = cv2.boundingRect(p)
    return (x,y,w,h)