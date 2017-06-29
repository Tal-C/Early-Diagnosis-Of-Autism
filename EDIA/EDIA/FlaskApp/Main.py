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

        total_smiles_detected = vid_analizer.getTotalSmilesDetected()
        smiles_detected_in_sequence = vid_analizer.getSmilesInSequence()
        eyes_movement = vid_analizer.getEyesMovement()
        head_movement = vid_analizer.getHeadMovement()
        num_of_frames = vid_analizer.getNumOfFrames()
        running_time = (time.time() - start_time) / 60

        # Write Charts.js:
        html_file = open("FlaskApp/templates/uploaded_file.html", 'w')
        
        html_str = """
        <!DOCTYPE html>
<html lang = "en" xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta charset = "utf-8" />
        
        <title>EDOA - Data Report</title > 

        <link rel = "stylesheet" href="{{url_for('static',filename='css/jquery.mobile-1.4.5.css')}}">
        <!--Icon title-->
        <link rel = "icon" href="{{ url_for('static', filename='img/logo_trans.png') }} " type = "image/png" />

        <!-- Charts: -->
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        
		<!-- jQuery: -->
		<script src="../static/js/jquery.min.js"></script>

        <script>
            google.charts.load("current", { packages: ["corechart"] });
            google.charts.setOnLoadCallback(drawChart);

            function drawChart() {
                var data = google.visualization.arrayToDataTable([
                    ["Element", "Percentage", { role: "style" }],
        """
        # Adding variables into chart:
       
        html_str += "\t\t\t['Total smiles', {}, ".format(total_smiles_detected)
        if (total_smiles_detected < 50):
            html_str += "'#ff0000'"
        else:
            html_str += "'#ba4bff'"
        html_str += "],\n"

        html_str += "\t\t\t['Smiles in sequence', {}, ".format(smiles_detected_in_sequence)
        if (smiles_detected_in_sequence < 50):
            html_str += "'#ff0000'"
        else:
            html_str += "'#ba4bff'"
        html_str += "],\n"

        html_str += "\t\t\t['Eyes movement', {}, ".format(eyes_movement)
        if (eyes_movement < 50):
            html_str += "'#ff0000'"
        else:
            html_str += "'#ba4bff'"
        html_str += "],\n"

        html_str += "\t\t\t['Head movement', {}, ".format(head_movement)
        if (head_movement < 50):
            html_str += "'#ff0000'"
        else:
            html_str += "'#ba4bff'"
        html_str += "]\n"

        html_str += """
                ]);
            var view = new google.visualization.DataView(data);
                view.setColumns([0, 1,
                                 {
                                     calc: "stringify",
                                     sourceColumn: 1,
                                     type: "string",
                                     role: "annotation"
                                 },
                                 2]);

                var options = {
                    title: "Diagnosis Details:",
                    width: 1000,
                    height: 400,
                    bar: { groupWidth: "80%" },
                    legend: { position: "none" },
                };

                var chart = new google.visualization.BarChart(document.getElementById("barchart_values"));
                chart.draw(view, options);
            }
        </script>
		
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
			
			#barchart_values {
				margin-bottom: 120px;
			}
            
        </style>
    </head>
    <body background="../static/img/1.png">
        <center><h1 class="font-style">EDOA - Data Report</h1></center>
        <hr/><br/>
        
        <center>
            <div id="barchart_values" style="width: 900px; height: 300px;"></div>
        """

        html_str += "<div><h2>Number Of Frames: {}</h2></div>".format(num_of_frames)
        html_str += "<div><h2>System Running Time: %.3f Minutes</h2></div>" % (running_time)
      
        html_str += """
        </center>
    </body>
</html>
        """

        html_file.write(html_str)
        html_file.close

        return video_name
     
