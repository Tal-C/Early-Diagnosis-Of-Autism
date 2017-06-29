
import wave
import os
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import pyaudio as pa
import audioop
import scipy
from scipy.io import wavfile as wav
#from sklearn.decomposition import FastICA, PCA
#import time
#import speech_recognition as sr
import pocketsphinx
from scipy.signal import butter, lfilter, freqz
from pydub import AudioSegment
import pydub
from mdp import fastica
#API_KEY = "G4NEkOrcj5"
class AudioAnalyzer(object):

    def __init__(self, name):
        self.file_path = name + ".mp3"
        self.file_name = name.split('.')[0]
        self.file_name = self.file_name.split('/')[1]
        
        if not self.check_file(self.file_path):
            return
        #inits to wave reader
        self.convert_to_wave(self.file_path,self.file_name)
        self.wr = wave.open(os.getcwd() + "\\content\\" + self.file_name + ".wav",'r')
        self.audio_frames = self.wr.getnframes()
        self.channel = self.wr.getnchannels()
        self.fs = self.wr.getframerate()
        self.duration = self.audio_frames/self.fs
        self.wr.close()

    def convert_to_wave(self,file_path,file_name):
        subprocess.call(['ffmpeg', '-i', os.getcwd() + "\\content\\" + self.file_name + '.mp3',
                         os.getcwd() + "\\content\\" + self.file_name + '.wav'])
        ##Delete the mp3 unnessery file
        try:
            os.remove(os.getcwd() + "\\content\\" + self.file_name + '.mp3')
        except OSError:
            pass
    def butter_lowpass(self,cutoff, fs, order=1):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        coeff_b, coeff_a = butter(order, normal_cutoff, btype='low', analog=False)
        
        return coeff_b, coeff_a

    def butter_lowpass_filter(self,data, cutoff, fs, order=1):
        coeff_b, coeff_a = self.butter_lowpass(cutoff, fs, order)
        y = lfilter(coeff_b, coeff_a, data)
        return y
   
    def reduce_noices(self):
        
        self.fs,self.data = wav.read(os.getcwd() + "\\content\\" + self.file_name + ".wav")
        wr = wave.open(os.getcwd() + "\\content\\" + self.file_name + ".wav",'r')
        lowpass = 30 #Hz - Remove lower frequencies
        
        signal = np.fromstring(wr.readframes(self.audio_frames), dtype=np.int16)
        ########PLOTING###################
        #Time = np.linspace(0, self.audio_frames / self.smplrate, num=len(signal))    
        ###################################
        #data that doesn’t contain complex numbers but just real numbers.
        signalfft = np.fft.rfft(signal)
        coeff_b, coeff_a, = self.butter_lowpass(lowpass, self.fs)
        y = self.butter_lowpass_filter(signalfft, lowpass, self.fs)
       
        filtered_signal = np.fft.irfft(y).astype(int)#DFT
        t = np.linspace(0, self.duration, len(filtered_signal), endpoint=False)
        #ns = np.column_stack((nl,nr)).ravel().astype(np.int16)
        #print(type(ns))
        #ns = ns.tolist()
        #Plotting for lowpass filter
        plt.figure(1)
        plt.subplot(411)
        w, h = freqz(coeff_b, coeff_a, worN=8000)
        plt.plot(0.5 * self.fs * w / np.pi, np.abs(h), 'b')
        plt.plot(lowpass, 0.5 * np.sqrt(2), 'ko')
        plt.axvline(lowpass, color='k')
        plt.xlim(0, 0.5 * self.fs)
        plt.title('Lowpass Filter')
        plt.xlabel('Frequency [Hz]')
        plt.grid()

        plt.subplot(413)
       
        plt.plot( t,signal, 'b-', label='data')
        plt.plot(t,filtered_signal, 'g-', linewidth=2, label='filtered data')
        plt.xlabel('Time [sec]')
        plt.grid()
        plt.title('Lowpass Filter Frequency Response ')
        #plt.legend()
        plt.savefig(os.getcwd() + "\\content\\lowpass.png")
        wav.write(os.getcwd() + "\\content\\" + self.file_name + "_filtered.wav",self.fs,filtered_signal)


    
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
    def split_audio(self):
        self.fs,self.data = wav.read(os.getcwd() + '\\content\\' + self.file_name + '.wav')

        ww = wave.open(os.getcwd() + "\\content\\" + self.file_name + ".wav",'wb')
        voices = []
        #FastICA - to separate channels and waves
        source = fastica(self.data.astype(float))
        #normalize
        source = np.int16(source / np.max(abs(source),axis=0) * 32767)

        #plt.plot(np.array(source))
        #plt.savefig(os.getcwd() + "\\content\\fastICA_plot.png")

        #Creating mono channele files:
        wav.write(os.getcwd() + '\\content\\'+self.file_name+'_ICAleft.wav',44100,source[:,0])
        wav.write(os.getcwd() + '\\content\\'+self.file_name+'_ICAright.wav',44100,source[:,1])
        ##########################PLOTTING#######################################
        plt.figure(1)
        plt.subplot(511)
        plt.title("fastICA")
        plt.plot(source)
        plt.subplot(513)
        plt.title("fastICA-left channel")
        plt.plot(source[:,0])
        plt.subplot(515)
        plt.title("fastICA - right channel")
        
        plt.plot(source[:,1],color='orange')

        plt.savefig(os.getcwd() + "\\content\\fastICA.png")
        ###########################SEPARATE VOICES##############################################
        #chunk = 1024#buffer
        #self.treshold = audioop.avg(self.data, 2) #treshold for silence
        #rms = 0 ## root-mean-square -> measure of the power in an audio signal.
        #i = 0
        eps = 200
        #for i in range(len(source)):
        pos = []
        pos.append(0)
        i = 1
        value = 0
        #while True:
        #    while np.linalg.norm(source[i],ord=2) <= eps and i < len(source):
        #        value = i
        #        i += 1
        #    if(np.linalg.norm(source[i],ord=2) > eps):
        #        if(pos[i-1] == 0):
        #            i+=1
        #            continue
        #        else: pos.append(value)
        #        i+=1
        #        continue
        #    if(i ==  len(source) -1):
        #        break
        #print(pos)    
        #while rms < self.treshold:
        #    index = i*22050
        #    rms = max(self.data[index][0],self.data[index][1]) #check each 0.5 second
        #    i+=1
        #frames = []
        #pos = []
        #sec = 0
        #self.wr = wave.open(os.getcwd() + "\\content\\" + self.file_name + ".wav",'r')

        #while rms > self.treshold:
        #    #sec+=1
        #    data = self.wr.readframes(chunk)
        #    print("Data = ",len(data))
        #    rms = audioop.rms(data,2)
        #    #pos.append(sec)
        #    frames.append(data)
            
        #    #if(rms == 0 and data ==""):
        #    #    pos.append(sec)
        #    #    break
        #    #elif(rms == 0):
        #    #    pos.append(sec)

        #print(len(frames))
        #print(pos)
        
    
    def close_streams(self):
        try:
            os.remove(os.getcwd() + "\\content\\" + self.file_name + '.wav')
        except oserror:
            pass
        


