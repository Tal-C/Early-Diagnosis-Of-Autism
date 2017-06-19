#import acoustid
#import pyaudio
import wave
import os
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import pyaudio as pa
import audioop


#API_KEY = "G4NEkOrcj5"
class AudioAnalyzer(object):

    def __init__(self, name):
        self.file_path = name + ".mp3"
        self.file_name = name.split('.')[0]
        self.file_name = self.file_name.split('/')[1]
        self.threshold = 20
        self.channel = 1
        #self.audio = pa.PyAudio()
        
        if not self.check_file(self.file_path):
            return
         
        self.create_audio_reader(self.file_path,self.file_name)


    def create_audio_reader(self,file_path,file_name):
        subprocess.call(['ffmpeg', '-i', os.getcwd() + "\\content\\" + self.file_name + '.mp3',
                         os.getcwd() + "\\content\\" + self.file_name + '.wav'])
        ##Delete the mp3  unnessery file
        try:
            os.remove(os.getcwd() + "\\content\\" + self.file_name + '.mp3')
        except OSError:
            pass
       
    def reduce_noices(self):
        
        wr = wave.open(os.getcwd() + "\\content\\" + self.file_name + ".wav",'r')
        self.ww = wave.open(os.getcwd() + '\\content\\filtered_' + self.file_name + '.wav', 'w')

        self.audio_frames = wr.getnframes()
        self.smplrate = wr.getframerate() # Read and process 1 second at a time.
        
        lowpass = 21 #Hz - Remove lower frequencies
        
        duration = int(self.audio_frames / self.smplrate) # whole length file 
        for num in range(duration):
            print('Processing {}/{} s'.format(num+1, duration))
            signal = np.fromstring(wr.readframes(self.smplrate), dtype=np.int16)
            left, right = signal[0::2], signal[1::2] # left and right channel
            ########PLOTING###################
            Time = np.linspace(0, self.audio_frames / self.smplrate, num=len(signal))    
            plt.figure(1)
            plt.title('Signal Wave...')
            plt.plot(Time,signal)
            plt.savefig('sample-graph.png')
            ###################################

            #data that doesn’t contain complex numbers but just real numbers.
            lf, rf = np.fft.rfft(left), np.fft.rfft(right)
            lf[:lowpass], rf[:lowpass] = 0, 0 # low pass filter
            lf[55:66], rf[55:66] = 0, 0 # line noise
            nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)#DFT
            ns = np.column_stack((nl,nr)).ravel().astype(np.int16)
            #print(type(ns))
            ns = ns.tolist()
            #self.ww.writeframes("".join(ns))
           
        wr.close()
        #self.ww.close()
        ######################################################
        ###############TO uncommnent
        #try:
        #    os.remove(os.getcwd() + "\\content\\" + self.file_name + '.wav')
        #except OSError:
        #    pass
        ######################################################
        return             

    def check_file(self, file_name):
        list = file_name.split('.')
        if list[len(list) - 1] != "mp3":
            print "Invalid file. File must be a mp3 file"
            return False
        if not os.path.isfile(file_name):
            print "File does not exists"
            return False
        return True 
    ##Returns array duration of each speach
    def split_audio(self,):
        wr = wave.open(os.getcwd() + "\\content\\" + self.file_name + ".wav",'r')
        signal = np.fromstring(wr.readframes(self.smplrate), dtype=np.int16)
        while True:
            data = wr.readframes(self.audio_frames)
            rms = audioop.rms(data,2)
            if(rms > self.threshold):
                break
        
        wr.rewind()
        #Storing frames:
        frames = []
        #records upto silence only
        while rms > self.threshold:
            data = wr.readframes(self.audio_frames)
            rms = audioop.rms(data,2)
            frames.append(data)

        print("Finishing recording...writing file...")
        write_frames = wave.open(os.getcwd()+"\\content\\"+self.file_name+"_part"+".wav", 'wb')##change to 'filtered'
        write_frames.setnchannels(self.channel)
        write_frames.setsampwidth(wr.getsampwidth())
        write_frames.setframerate(self.smplrate)
        write_frames.writeframes(''.join(frames))
        write_frames.close()
        wr.close()
              