import acoustid
import pyaudio
import wave
import os
import numpy as np
import matplotlib.pyplot as plt

#API_KEY = "G4NEkOrcj5"
class AudioAnalyzer(object):

    def __init__(self, name):
        self.file_path = name+".wav"
        self.file_name = self.file_path.split('/')[1]
        if not self.check_file(self.file_path):
            return
         
        self.create_audio_reader(self.file_path,self.file_name)


    def create_audio_reader(self,file_path,file_name):
        self.reduce_noices(file_path,file_name)


    def reduce_noices(self,file_path,file_name):
        
        wr = wave.open(file_name,'r')
        
        self.audio_frames = wr.getnframes()
        self.smplrate = wr.getframerate()

        sHz = self.smplrate
        da = np.fromstring(wr.readframes(sHz), dtype=np.int16)
        left, right = da[0::2], da[1::2]
        #data that doesn’t contain complex numbers but just real numbers.
        lf, rf = np.fft.rfft(left), np.fft.rfft(right)
        plt.figure(1)
        a = plt.subplot(211)
        r = 2**16/2
        a.set_ylim([-r, r])
        a.set_xlabel('time [s]')
        a.set_ylabel('sample value [-]')
        x = np.arange(44100)/44100
        plt.plot(x, left)
        b = plt.subplot(212)
        b.set_xscale('log')
        b.set_xlabel('frequency [Hz]')
        b.set_ylabel('|amplitude|')
        plt.plot(abs(lf))
        #plt.savefig('sample-graph.png')
        plt.show()


        
             

    def check_file(self, file_name):
        list = file_name.split('.')
        if list[len(list) - 1] != "wav":
            print "Invalid file. File must be a mp3 file"
            return False
        if not os.path.isfile(file_name):
            print "File does not exists"
            return False
        return True       