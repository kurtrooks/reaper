#!/usr/bin/env python
import pygame
import rospy
import glob
import sys
import random
from std_msgs.msg import *


class audio_driver(object):

    def __init__(self):
        rospy.init_node('audio_driver')
 
        self.hz = rospy.get_param('~hz',40.0)
        self.rate = rospy.Rate(self.hz)
        self.audioDir = rospy.get_param('~audio_dir',None)
        self.audio_files = []

        if self.audioDir != None:
            self.loadAudio(self.audioDir)
        else:
            print "No audio directory specified"

        rospy.Subscriber('trigger_sound',Bool,self.triggerSound)

    def loadAudio(self,audio_dir):
        print "Attempting to load audio from",audio_dir

        for file in glob.glob(audio_dir + '/*.wav'):
	    self.audio_files.append(file)

        print self.audio_files
	pygame.init()
	pygame.mixer.init()

    def triggerSound(self,trigger):
        if len(self.audio_files) == 0:
            return

	random_sound = random.choice(self.audio_files)

	pygame.mixer.music.load(random_sound)
	pygame.mixer.music.play()


    def run(self):
        while not rospy.is_shutdown():
            self.rate.sleep()    

if __name__ == "__main__":
    node = audio_driver()
    node.run()
