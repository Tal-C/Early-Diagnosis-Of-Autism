from VideoAnalizer import VideoAnalizer
from VideoAnalizer import camera_capture
import time
import cv2 

class Main():
    """ The main class of the project.
        The class sends videos to analize. """
    # list of video files
    ## save a video usinf computer camera
    #camera_capture("content/rivka11")
    def __init__(self):
        return

    def vid_Analizer(self,video_name):
        files_list = ('content/%s'%video_name, None)
        #files_list = ('content/Katia', None) #-------- Original
        for name in files_list:
            start_time = time.time()
            vid_analizer = VideoAnalizer('%s' % (name),False)
            if vid_analizer.cap is None:
                continue
            vid_analizer.read_video(name)
            f = open('%s_output.txt' % name, 'a')  
            print >> f," system running time: %s minutes" % ((time.time() - start_time) / 60)
            f.close()