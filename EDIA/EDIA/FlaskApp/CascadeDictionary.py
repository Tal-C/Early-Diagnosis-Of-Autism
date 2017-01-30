import numpy as np
import cv2

# a tuple of the cascades we are going to use
tuple = ('haarcascade_frontalface_default', 'haarcascade_profileface', 'haarcascade_eye', 'haarcascade_mcs_eyepair_big', 'haarcascade_smile',
         'haarcascade_mcs_mouth', 'haarcascade_mcs_nose', 'haarcascade_mcs_leftear', 'haarcascade_mcs_rightear')
# the path to the xml files folder
folder_path = 'C:/Users/owner/Documents/opencv/sources/data/haarcascades/'

my_list = []    # a list of the xml files
d = {}          # a dictionary which contains for each cascade the appropriate object

# add the folder path to each file
for i in range(len(tuple)):
    my_list.append("%s%s.xml"%(folder_path, tuple[i]))

# create the cascade appropriate object
for i in range(len(tuple)):
    d[tuple[i]] = cv2.CascadeClassifier(my_list[i])