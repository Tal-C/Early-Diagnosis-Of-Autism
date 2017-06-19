from VideoAnalizer import VideoAnalizer
from VideoAnalizer import camera_capture
import time
import cv2 
import codecs


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

        vid_analizer = VideoAnalizer('%s' %file_path,False)
        
        if vid_analizer.cap is None:
           return 404   #Cannot find the file

        vid_analizer.read_video(file_path)
        f = open('%s_output.txt' % file_path, 'a')  
        print >> f,"System running time: %.3f minutes" % ((time.time() - start_time) / 60)

        f.close()

        report_str = vid_analizer.get_report_str()
        report_str += "\nSystem running time: %.3f minutes" % ((time.time() - start_time) / 60)

        #print(report_str)

        html_file = open("C:\\Users\\Katia\\Source\\Repos\\Diagnosis-of-Autism\\EDIA\\EDIA\\FlaskApp\\templates\\uploaded_file.html", 'w')

        html_str = """
<!DOCTYPE html>
<html lang = "en" xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta charset = "utf-8" />
        
        <title>EDOA - Data Report</title > 

        <link rel = "stylesheet" href="{{url_for('static',filename='css/jquery.mobile-1.4.5.css')}}">
        <!--Icon title-->
        <link rel = "icon" href="{{ url_for('static', filename='img/logo_trans.png') }} " type = "image/png" />
        
        <script src = "{{ url_for('static', filename='js/jquery.min.js') }}" > </script>
        <script src = "{{url_for('static',filename='js/jquery-1.10.2.js')}}" > </script> 
        
        <style>
			img {
				opacity: 0.2;
				filter: alpha(opacity=50); /* For IE8 and earlier */
			}
            .font-style { 
                font-style: italic;
            }
            hr { 
                display: block;
                margin-top: 0.5em;
                margin-bottom: 0.5em;
                margin-left: auto;
                margin-right: auto;
                border-style: inset;
                border-width: 2px;
            }
        </style>
    </head>
    <body background="../static/img/1.png" ><center>
        <center><h1 class="font-style">EDOA - Data Report</h1></center>
        <hr/><br/>
        """

        report_str_arr = report_str.split("\n");
        for s in report_str_arr:
            html_str += "\n\t\t<h2>" + s + "</h2>\n<br/>"
        
        html_str += """
    </center></body>
</html>
        """

        html_file.write(html_str)
        html_file.close()

#        html_file =
#        open("C:\Users\tal\Source\Repos\Diagnosis-of-Autism\EDIA\EDIA\FlaskApp\templates\uploaded_file.html",
#        'r+')
#        html_lines = html_file.readlines()
#        print(html_lines)
#        html_lines.insert(0, report_str)

#        html_file =
#        open("C:\Users\tal\Source\Repos\Diagnosis-of-Autism\EDIA\EDIA\FlaskApp\templates\uploaded_file.html",
#        'w')
#        html_file.writelines(html_lines)
#        html_file.close()
#        report_file.close()

        return video_name
     
