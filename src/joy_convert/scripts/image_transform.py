#!/usr/bin/env python

import rospy
from sensor_msgs.msg import *
from std_msgs.msg import *

from Queue import Queue

class image_transform(object):

    def __init__(self):
        rospy.init_node('image_transform')
        self.hz = rospy.get_param('~hz',40.0)
        self.rate = rospy.Rate(self.hz)
        self.minAngle = rospy.get_param('~minAngle',550)
        self.maxAngle = rospy.get_param('~maxAngle',2500)
        self.minPixel = rospy.get_param('~minPixel',0)
        self.maxPixel = rospy.get_param('~maxPixel',1260)
        self.invert = rospy.get_param('~invert',False)

        self.halfRange = (self.maxAngle - self.minAngle) / 2.0
        self.midAngle = self.minAngle + self.halfRange

        self.halfPixel = (self.maxPixel - self.minPixel) / 2.0
        self.midPixel = (self.minAngle + self.halfPixel)

	self.myX = None
	self.myY = None

        rospy.Subscriber('input',UInt16,self.setX)
        self.servoPub = rospy.Publisher('servo',UInt16,queue_size=10)

    def setX(self,msg):
	self.myX = msg.data
        self.setPub()

    def interp(self,xval):
        """
        roughly 640 is midPixel
        so (xval / maxPixel) --> 0 to 1
        """
        rval = float(xval/float(self.maxPixel))
        return rval

    def angleinterp(self,data):
        """
        0-->1 input
        """
        return self.minAngle + (data*self.maxAngle - self.minAngle)

    def setPub(self):
	if(self.myX is not None):
            myMessage = self.interp(self.myX)
            print(myMessage)
            myMessage = self.angleinterp(myMessage)
        else:
            return

        if self.invert:
            myMessage = -1.0*myMessage

        self.servoPub.publish(myMessage)

    def run(self):

        while not rospy.is_shutdown():
            self.rate.sleep()    

if __name__ == "__main__":
    node = image_transform()
    node.run()
