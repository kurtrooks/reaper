#!/usr/bin/env python

import rospy
import subprocess
from std_msgs.msg import *

class eye_ctrl(object):
    def __init__(self):

        rospy.init_node('eye_ctrl')

        # Params
        self.hz = rospy.get_param('~hz',1.0)
        self.rate = rospy.Rate(self.hz)
        self.eyeCmd = rospy.get_param('~eye_cmd','./eyes.py')

        # Subs
        rospy.Subscriber('enable',Bool,self.setEnable)
    
        self.pipe='/tmp/eyepipe.fifo'

    def setEnable(self,msg):
        if msg.data == True:
            self.eyesOn()
        else:
            self.eyesOff()

    def eyesOn(self):
        print "eyes ON"
        try:
#            subprocess.call([self.eyeCmd, "100", "0", "0"])
            with open(self.pipe, 'w') as f:
                f.write('on')
                f.flush()
        except Exception as ex:
            print ex

    def eyesOff(self):
        print "eyes OFF"
        try:
#            subprocess.call([self.eyeCmd, "0", "0", "0"])
            with open(self.pipe, 'w') as f:
                f.write('off')
                f.flush()
        except Exception as ex:
            print ex

    def run(self):
        while not rospy.is_shutdown():
            self.rate.sleep()

if __name__ == "__main__":
    node = eye_ctrl()
    node.run()
