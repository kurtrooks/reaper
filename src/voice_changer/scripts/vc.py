#!/usr/bin/env python

import pyaudio
from numpy.fft import fft,ifft,rfft,irfft
import numpy as np
import struct

CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 20

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(WIDTH),
        channels=CHANNELS,
        rate=RATE,
        input=True,
        output=True,
        frames_per_buffer=CHUNK)

print("* recording")

#for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
while True:    
    try:
        data = stream.read(CHUNK)
        npdata = np.frombuffer(data,dtype=np.int16)
        sig = irfft(fft(npdata))
        #out = np.real(sig)
        #print type(out),out
        
        sig = sig.astype(np.float32).tostring()

        #print sig,type(sig)
        #exit()
        #data_bits = shift_data.astype('uint8')
        #out_data = shift_data.tostring(shift_data)        
        #print data_bits
        #exit()
        #out_data = shift_data.astype(np.float32).tostring()
        stream.write(sig, CHUNK)   
    except Exception as ex:
        print ex

print("* done")

stream.stop_stream()

stream.close()

         
p.terminate()
