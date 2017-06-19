from VideoAnalizer import VideoAnalizer
from VideoAnalizer import camera_capture
import time
import cv2 
import codecs

#from hachoir_parser import createParser
#from hachoir_metadata import extractMetadata

class Main():
    """ The main class of the project.
        The class sends videos to analize. """
    # list of video files
    ## save a video usinf computer camera
    
    def __init__(self):
        return

    def vid_Analizer(self,video_name):
        file_path = 'content/%s' % video_name
        #files_list = ('content/Katia', None) #-------- Original
        #for name in files_list:
        start_time = time.time()

        #vid_analizer = VideoAnalizer('%s' %file_path,False)
        
        #if vid_analizer.cap is None:
        #   return 404   #Cannot find the file

        #vid_analizer.read_video(file_path)
        #f = open('%s_output.txt' % file_path, 'a')  
        #print >> f,"System running time: %.3f minutes" % ((time.time() - start_time) / 60)

        #f.close()

        #report_str = vid_analizer.get_report_str()
        #report_str += "\nSystem running time: %.3f minutes" % ((time.time() - start_time) / 60)

        #total_smiles_detected = vid_analizer.getTotalSmilesDetected()
        #smiles_detected_in_sequence = vid_analizer.getSmilesInSequence()
        #eyes_movement = vid_analizer.getEyesMovement()
        #head_movement = vid_analizer.getHeadMovement()
        #num_of_frames = vid_analizer.getNumOfFrames()
        #running_time = (time.time() - start_time) / 60

        #print "total smiles: {}".format(total_smiles_detected)
        #print "seq smiles: {}".format(smiles_detected_in_sequence)
        #print "eyes movement: {}".format(eyes_movement)
        #print "head movement: {}".format(head_movement)
        #print "num of frames: {}".format(num_of_frames)
        #print "running time: {}".format(running_time)
        
        return video_name
     
