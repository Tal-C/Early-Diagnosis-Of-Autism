import Main
import MySQLConnector
class Video_Controller():

    def __init__(self):
        return

    def video_handler(self,video_name,user_id):
        #after first checking of video type on API:
        videoptr = Main.Main()
        resp_video = videoptr.vid_Analizer(str(video_name))#returns video on access
        #insert database
        mysqlptr = MySQLConnector.MySQL_Connector()
        params = (int(user_id),str(resp_video),str(''))
        resp_db = mysqlptr.ExecuteSP_Params('sp_insert_video_by_user_id',params)
        return

    def video_all(self):
        mysqlptr = MySQLConnector.MySQL_Connector()
        resp_db = mysqlptr.ExecuteSP('sp_get_all_videos')
        return resp_db