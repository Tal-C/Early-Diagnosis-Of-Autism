from VideoAnalizer import VideoAnalizer
from VideoAnalizer import camera_capture
import time
import cv2 

from hachoir_parser import createParser
from hachoir_metadata import extractMetadata

class Main():
    """ The main class of the project.
        The class sends videos to analize. """
    # list of video files
    ## save a video usinf computer camera
    
    def __init__(self):
        return

    def vid_Analizer(self,video_name):
        file_path = 'content/%s'%video_name
        #files_list = ('content/Katia', None) #-------- Original
        #for name in files_list:
        start_time = time.time()

        vid_analizer = VideoAnalizer('%s' %file_path,False)
        
        if vid_analizer.cap is None:
           return 404#Cannot find the file
       #read the video after all checks
        s = vid_analizer.read_video(file_path)
        f = open('%s_output.txt' % file_path, 'a')  
        print >> f," system running time: %s minutes" % ((time.time() - start_time) / 60)
        f.close()
        return video_name