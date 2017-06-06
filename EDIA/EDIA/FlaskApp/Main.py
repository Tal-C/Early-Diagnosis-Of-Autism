from VideoAnalizer import VideoAnalizer
from VideoAnalizer import camera_capture
import time
import cv2 

class Main():
    """ The main class of the project.
        The class sends videos to analize. """
    # list of video files
    ## save a video using computer camera
    #camera_capture("content/rivka11")
    def __init__(self):
        return

    def vid_Analizer(self,video_name):
        file_path = 'content/%s'%video_name
        #files_list = ('content/Katia', None) #-------- Original
        #for name in files_list:
        start_time = time.time()
        vid_analizer = VideoAnalizer('%s' %file_path,False)
        if vid_analizer.cap is None:
           return 404#Cannot find th file
        vid_analizer.read_video(file_path)
        f = open('%s_output.txt' % file_path, 'a')  
        print >> f," system running time: %s minutes" % ((time.time() - start_time) / 60)
        f.close()
        return video_name