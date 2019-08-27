#!/usr/bin/env python
import numpy as np
import rospy
from std_msgs.msg import *

class sin_generator(object):

    def __init__(self):
        rospy.init_node('sin_gen')
       
        self.samplingFreq = rospy.get_param('~sampling_freq',60.0) # samples/sec
        self.rate = rospy.Rate(self.samplingFreq)
        self.sinPeriod = rospy.get_param('~sin_period',1.0) # sec
        self.amplitude = rospy.get_param('~amplitude',90.0)
        self.outputOffset = rospy.get_param('~outputOffset',90.0)
        self.enabled = rospy.get_param('~start_running',False)

        self.waveformPub = rospy.Publisher('waveform',UInt16,queue_size=10)
        self.genWaveform()

        self.i = 0

        rospy.Subscriber('setEnable',Bool,self.setEnable)
        rospy.Subscriber('setPeriod',Float64,self.setPeriod)
        rospy.Subscriber('setAmplitude',Float64,self.setAmplitude)

    def setOffset(self,msg):
        self.outputOffset = msg.data
        self.genWaveform()

    def setAmplitude(self,msg):
        self.amplitude = msg.data
        self.genWaveform()

    def setPeriod(self,msg):
        self.sinPeriod = msg.data
        self.genWaveform()

    def setEnable(self,msg):
        self.enabled = msg.data

    def genWaveform(self):
        prevEn = self.enabled
        self.enabled = False

        Fs = self.samplingFreq # sampling freq
        freq = 1/self.sinPeriod # sin freq

        # Generate sin wave
        x = np.arange(Fs/freq)
        self.waveform = self.amplitude*np.sin(np.pi*2.0*freq*x/Fs) 
        self.enabled = prevEn

    def run(self):

        while not rospy.is_shutdown():

            self.rate.sleep()

            if self.enabled is True:
                    output = int(self.waveform[self.i])
                    output += int(self.outputOffset)
                    if output < 0:
                        output = 0

                    self.waveformPub.publish(int(output))
                    self.i += 1
                    if self.i >= len(self.waveform):
                        self.i = 0

if __name__ == '__main__':
    try:
        node = sin_generator()
        node.run()
    except Exception as ex: 
       print ex 
