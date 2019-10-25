#!/usr/bin/env python

import rospy
from sensor_msgs.msg import *
from std_msgs.msg import *

class image_transform(object):

    def __init__(self):
        rospy.init_node('image_transform')
        self.hz = rospy.get_param('~hz',10.0)
        self.rate = rospy.Rate(self.hz)
        self.minAngle = rospy.get_param('~minAngle',0)
        self.maxAngle = rospy.get_param('~maxAngle',180)
        self.minPixel = rospy.get_param('~minAngle',0)
        self.maxPixel = rospy.get_param('~maxAngle',1260)
        self.invert = rospy.get_param('~invert',False)

        self.halfRange = (self.maxAngle - self.minAngle) / 2.0
        self.midAngle = self.minAngle + self.halfRange

        self.halfPixel = (self.maxPixel - self.minPixel) / 2.0
        self.midPixel = (self.minAngle + self.halfPixel)

	self.myX = None
	self.myY = None

        rospy.Subscriber('image_x',UInt16,self.setX)
        rospy.Subscriber('image_y',UInt16,self.setY)
        self.servoPub = rospy.Publisher('servo',UInt16,queue_size=10)

    def setX(self,msg):
	self.myX = msg.data
    def setY(self,msg):
	self.myY = msg.data

    def interp(self,xval):
        return xval / (self.midPixel)
    def angleinterp(self,data):
        """
        0-->2 input
        """
        data = data/2.0
        return data/self.midAngle

    def setPub(self):
	if(self.myX is not None and self.myY is not None):
            myMessage = interp(self.myX)
            myMessage = angleinterp(myMessage)

        if self.invert:
            myMessage = -1.0*myMessage

        self.servoPub.publish(int(myMessage))

    def run(self):

        while not rospy.is_shutdown():
            self.rate.sleep()    

if __name__ == "__main__":
    node = image_transform()
    node.run()
