import Main

class Video_Controller():

    def __init__(self):
        return

    def video_handler(self,video_name):
        #after first checking of video type on API:
        videoptr = Main.Main()
        resp = videoptr.vid_Analizer(str(video_name))
        return
