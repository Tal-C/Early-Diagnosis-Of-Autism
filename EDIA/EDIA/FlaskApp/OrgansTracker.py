import cv2
import numpy as np
from Face import calc_d
from collections import deque

class OrgansTracker(object):
    """description of class"""
    def __init__(self):
        LENGTH = 15
        # dictionary of eyes and nose centers deque
        self.centers = {"noses":deque(maxlen=LENGTH),
                        "r_eyes":deque(maxlen=LENGTH),
                        "l_eyes":deque(maxlen=LENGTH)}
        # count face/nose/eyes/smile in all frames
        self.counters = {"faces":0, "noses":0, "eyes":0, "smiles":0}
        self.no_smile = 0
        self.smiles_in_sequence = 0
        self.max_smiles_in_sequence = 0
        self.head_move = 0
        self.eyes_move = 0
        self.nose_dir = ""
        self.eyes_dir = ""
        self.smile_label = ""
        self.none = (-1,-1)
        self.report_str = ""

    # This function updates the organs variables
    def update_organs(self, faces):
        if len(faces) == 0:
            return
        self.counters["faces"] += 1
        face = faces[0]

        nose = face.get_nose_center()        
        nose = face.get_nose_center()
        if nose[0] != -1:
            self.counters["noses"] += 1

        r_center, self.r_radius, l_center, self.l_radius = faces[0].get_eyes_pupils()
        if self.r_radius != -1 or self.l_radius != -1:
            self.counters["eyes"] += 1
        
        self.update_centers("noses", nose)
        self.update_centers("r_eyes", r_center)
        self.update_centers("l_eyes", l_center)

        self.check_smile(face)
        
    # This function updates the organs centers lists
    def update_centers(self, list_name, object):
        list = self.centers[list_name]
        if len(list) < 3 or object == self.none:
            list.appendleft(object)
            return
        l = np.array(list)
        x = l[:,0]
        y = l[:,1]
        is_none = x == -1
        x = np.delete(x,np.where(is_none == True))
        y = np.delete(y,np.where(is_none == True))
        if len(x) < 3:
            list.appendleft(object)
            return
        x_med = int(np.median(x))
        y_med = int(np.median(y))
        d = calc_d((x_med,y_med),object)
        if d < 80:
            list.appendleft(object)
    
    # This function check if there's a smile in the frame and sets the smile label respectively
    def check_smile(self, face):
        if face.get_smile() is not None:
            self.smile_label = "smile"
            self.smiles_in_sequence += 1
            self.counters["smiles"] += 1
        else:
            self.smile_label = ""
            self.no_smile += 1
            if self.no_smile > 3:
                self.no_smile = 0
                if self.smiles_in_sequence > self.max_smiles_in_sequence:
                    self.max_smiles_in_sequence = self.smiles_in_sequence
                self.smiles_in_sequence = 0

    # This function write the labels in the frame 
    def add_labels(self, frame):
        cv2.putText(frame, "head: %s"%self.nose_dir, (10, 30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 1)
        cv2.putText(frame, "eyes: %s"%self.eyes_dir, (10, 60), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 1)
        cv2.putText(frame, self.smile_label, (10, 90), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 1) 
       
    # This function tracks organs and sets their labels
    def track(self, frame):
        x_direct = ""
        y_direct = ""

        self.nose_dx, self.nose_dy = 0,0
        x_direct, y_direct = self.track_organ(frame,"noses",(self.r_radius+self.l_radius)/2)
        if x_direct == -1:
            self.nose_dir = ""
        else:
            self.nose_dir = self.get_direction(x_direct, y_direct)
        
        r_x, r_y = self.track_organ(frame,"r_eyes",self.r_radius)
        l_x, l_y = self.track_organ(frame,"l_eyes",self.l_radius)
        if r_x != -1 and l_x != -1:
            x_direct = r_x if r_x == l_x else ""
            y_direct = r_y if r_y == l_y else ""
        elif r_x == -1 and l_x == -1:
            x_direct = ""
            y_direct = ""
        else:
            x_direct,y_direct = (r_x,r_y) if r_x != -1 else (l_x,l_y)
        self.eyes_dir = self.get_direction(x_direct, y_direct)

        if self.nose_dir != "":
            self.head_move += 1
        if self.eyes_dir != "":
            self.eyes_move += 1
    
    # This function tracks a given organ
    def track_organ(self, frame, list_name, radius):
        list = self.centers[list_name]
        epsilon = radius      # the minimum delta for movement
        x_direct, y_direct = "",""
        if list[0] != self.none:
            if list[-1] != self.none:
                center1 = list[0]
                center2 = list[-1]
                dx = center1[0] - center2[0] - self.nose_dx
                dy = center1[1] - center2[1] - self.nose_dy
                if dx != 0 and abs(dx) > epsilon:
                    x_direct = "left" if dx < 0 else "right"
                if dy != 0 and abs(dy) > epsilon:
                    y_direct = "upwards" if dy < 0 else "downwards"
        else:
            x_direct, y_direct = -1,-1
        for i in range(1,len(list)):
            if list[i-1] != self.none and list[i] != self.none:
                thickness = min(3,int(10 / i+1))
                cv2.line(frame, list[i - 1], list[i], (0, 0, 255), thickness)
        return x_direct,y_direct

    # This function returns the direction string
    def get_direction(self, x_direct, y_direct):
        if x_direct != "" and y_direct != "":
            return "%s-%s"%(x_direct,y_direct)
        elif x_direct != "":
            return x_direct
        return y_direct
  
    # This function prints the data into the text file
    def print_data(self, file_name, frames_num):
        s = ""
        self.max_smiles_in_sequence = max(self.max_smiles_in_sequence, self.smiles_in_sequence)
        d = self.counters
        f = open('%s_output.txt'%(file_name), 'w')  
        if frames_num > 10:
            # reduce 10 from sum because the track starts at frame 11
            print >> f, "smiles were detected in sequence at {0}% of the frames".format(int(float(self.max_smiles_in_sequence)/(d["faces"])*100))
            self.report_str += "smiles were detected in sequence at {0}% of the frames\n".format(int(float(self.max_smiles_in_sequence)/(d["faces"])*100))
            print >> f, "smiles were detected at {0}% of the frames".format(int(float(d["smiles"])/(d["faces"])*100))
            self.report_str += "smiles were detected at {0}% of the frames\n".format(int(float(d["smiles"])/(d["faces"])*100))
            print >> f, "eyes moves in {0}% of the frames".format(int(float(self.eyes_move)/(d["eyes"])*100))
            self.report_str += "eyes moves in {0}% of the frames\n".format(int(float(self.eyes_move)/(d["eyes"])*100))
            print >> f, "head moves in {0}% of the frames".format(int(float(self.head_move)/(d["noses"])*100))
            self.report_str += "head moves in {0}% of the frames\n".format(int(float(self.head_move)/(d["noses"])*100))
        else:
            print >> f, "video is too short"
        
        print >> f, "number of frames: ", frames_num
        self.report_str += "number of frames: {0}".format(frames_num) 

        f.close()   

    def get_report_str(self):
        return self.report_str