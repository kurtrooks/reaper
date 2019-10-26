#!/usr/bin/env python

import rospy
from std_msgs.msg import *

class eye_ctrl(object):

    def __init__(self):

        rospy.init_node('eye_ctrl')

        # Params
        self.hz = rospy.get_param('~hz',1.0)
        self.rate = rospy.Rate(self.hz)

        # Subs
        rospy.Subscriber('enable',Bool,self.setEnable)

    def setEnable(self,msg):
        if msg.data == True:
            self.eyesOn()
        else:
            self.eyesOff()

    def eyesOn(self):
        print "eyes ON"
        # TODO

    def eyesOff(self):
        print "eyes OFF"
        # TODO

    def run(self):
        while not rospy.is_shutdown():
            self.rate.sleep()

if __name__ == "__main__":
    node = eye_ctrl()
    node.run()
