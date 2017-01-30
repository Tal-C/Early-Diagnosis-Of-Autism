import os
import cv2
import numpy as np
import json
from ImageAnalizer import ImageAnalizer
from subprocess import call
import time
from Face import calc_d
from collections import deque
from OrgansTracker import OrgansTracker


class VideoAnalizer(object):
    """ This class receives a video, read it frame by frame and
        saves a new video which contains the information.
        Furthermore the class saves a text file with the baby movement
        information, and a jason file with the organs information """
    def __init__(self, file_name, rotate):
        if not self.check_file(file_name):
            self.cap = None
            return
        self.rotate = rotate
        self.cap = cv2.VideoCapture(file_name)
        self.create_video_writer(file_name)
        self.video_dict = {}

    # This function validates the input video
    def check_file(self, file_name):
        list = file_name.split('.')
        if list[len(list)-1] != "mp4":
            print "Invalid file. File must be a mp4 file"
            return False
        if not os.path.isfile(file_name):
            print "File dose not exists"
            return False
        return True

    # This function defines the codec and creates VideoWriter object
    def create_video_writer(self, file_name):
        name = os.path.splitext(file_name)[0]                       # define the new video name
        self.fps = self.cap.get(cv2.cv.CV_CAP_PROP_FPS)             # get video frames-per-second number
        width = int(self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))   # get video frames width and height
        height = int(self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
        # if video size is too large
        if width > 640:
            num = float(width)/640
            height = int(height/num)
            width = int(width/num)
        if self.rotate:
            size = (height,width)                                      # define new video frame size
        else:
            size = (width,height)
        fourcc = cv2.cv.CV_FOURCC(*'XVID')
        self.out = cv2.VideoWriter("%s_output.avi"%name ,fourcc, self.fps, size)

    # This function reads the video frame after frame
    def read_video(self, name):
        self.all_faces = {}
        prev_frame = None               # for the opticflow function
        prev_faces = deque(maxlen=2)    # to track organs using the two previous faces
        prev_faces.appendleft(None)   
        frame_num = 0
        organs_tracker = OrgansTracker()
        # loop to read frame by frame
        while(self.cap.isOpened()):
            ret, frame = self.cap.read()
            if not ret:
                break
            faces = []
            frame_num += 1
            # rotate the frame
            if self.rotate:
                frame = self.rotate_90(frame)  
            # if video size is too large                 
            if len(frame) > 640:
                frame = self.resize_image(frame,int(len(frame)/640))
            # search faces         
            img_analizer = ImageAnalizer(frame , prev_frame, prev_faces, frame_num)
            prev_frame = frame.copy()
            ## for privacy
            #frame = cv2.blur(frame,(17,17))
            img_analizer.mark_faces(frame)
            faces = img_analizer.faces
            if len(faces) == 0:
                faces = []
                prev_faces.appendleft(None)
            else:
                self.update_video_dict(faces[0], frame_num)
                organs_tracker.update_organs(faces)
                if frame_num > 10:
                    organs_tracker.track(frame)
                prev_faces.appendleft(faces[0])
            organs_tracker.add_labels(frame)
            # write to the output video
            self.out.write(frame)
            cv2.imshow('frame', frame)             
            # Display the resulting frame on screen
            if cv2.waitKey(int(self.fps)) & 0xFF == ord('q'):
                break

        # print movement information to the text file
        organs_tracker.print_data(name,frame_num)
        # print organs information to the jason file
        objects_json = json.dumps(self.video_dict)  #create jason object
        f = open('%s_objects.json'%(name), 'w')
        print >> f, objects_json
        f.close()

        self.release_memory()

    # This function rotates a given image 90 degrees to the right
    def rotate_90(self, img):
        cv2.flip(img, 0, img)
        return cv2.transpose(img)
    
    # This function resizes a given image
    def resize_image(self, img, num):    
        height, width, a = img.shape
        dim = (width/num, height/num)
        return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    
    # This function updates the dictionary of all organs
    def update_video_dict(self, face, frame_num):
        d = {}
        r_pupil = None
        l_pupil = None
        d['face'] = face.get_rect()
        for key,value in face.organs_dict.iteritems():
            if value != None:
                d[key] = value.get_rect()
                if key == 'r_eye':
                    r_pupil = value.get_pupil()
                    if r_pupil is not None:
                         d["r_pupil"] = r_pupil
                elif key == 'l_eye':
                    l_pupil = value.get_pupil()
                    if l_pupil is not None:
                        d["l_pupil"] = l_pupil
        self.video_dict[frame_num] = d

    def release_memory(self):        
        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()

# This function captures and saves a video from computer camera, and display it on the screen
def camera_capture(file_name):
    cap = cv2.VideoCapture(0)
    width = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))   # get video frames width and height
    height = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
    fps = 30.0
    size = (width,height)
    #Define the codec and create VideoWriter object
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    out = cv2.VideoWriter("%s.avi"%file_name ,fourcc, fps, size)
    while(cap.isOpened()):
        #Capture frame by frame
        ret, frame = cap.read()
        if ret != True:
            break
        out.write(frame)
        #Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
         
    cap.release()
    out.release()
    try:
        os.remove("%s.mp4"%file_name)
    except:
        pass
    os.rename("%s.avi"%file_name, "%s.mp4"%file_name)
    cv2.destroyAllWindows()