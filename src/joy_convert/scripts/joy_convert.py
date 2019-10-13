#!/usr/bin/env python

import rospy
from sensor_msgs.msg import *
from std_msgs.msg import *

class joy_convert(object):

    def __init__(self):
        rospy.init_node('joy_convert')
        self.hz = rospy.get_param('~hz',10.0)
        self.rate = rospy.Rate(self.hz)
        self.chNum = rospy.get_param('~chNum',0)
        self.minAngle = rospy.get_param('~minAngle',0)
        self.maxAngle = rospy.get_param('~maxAngle',180)
        self.invert = rospy.get_param('~invert',False)

        self.halfRange = (self.maxAngle - self.minAngle) / 2.0
        self.midAngle = self.minAngle + self.halfRange

        rospy.Subscriber('joy',Joy,self.setJoy)
        self.servoPub = rospy.Publisher('servo',UInt16,queue_size=10)

    def setJoy(self,msg):
        self.joy = msg
        left_stick = msg.axes[self.chNum]
        angle = self.midAngle + left_stick*self.halfRange

        if self.invert:
            angle = self.maxAngle - angle
        self.servoPub.publish(int(angle))

    def run(self):

        while not rospy.is_shutdown():
            self.rate.sleep()    

if __name__ == "__main__":
    node = joy_convert()
    node.run()
