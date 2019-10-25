#!/usr/bin/env python
import pygame
import rospy
import glob
import sys
import random
from std_msgs.msg import Bool

audio_files = []

def main():
	global audio_files
	for file in glob.glob("audio_files/*"):
		audio_files.append(file)

	audio_files = [i[12:] for i in audio_files]

	rospy.init_node('audio_driver_listener', anonymous=False)
	rospy.Subscriber('/audio_driver/scare_kids', Bool, audio_callback)

	pygame.init()
	pygame.mixer.init()

def audio_callback(msg):
	random_file = audio_files[0]
	if msg.data:
		random_file = random.choice(audio_files)

	pygame.mixer.music.load('/home/ubuntu/reaper/src/audio_driver/audio_files/' + random_file)
	pygame.mixer.music.play()


if __name__ == '__main__':
	main()
	while True:
		x = 5 #Placeholder
