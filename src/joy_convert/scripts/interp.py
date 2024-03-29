#!/usr/bin/env python

import rospy
from std_msgs.msg import *
from scipy import interpolate

class image_transform(object):

    def __init__(self):
        
        rospy.init_node('image_transform')
       
        # Params
        self.hz = rospy.get_param('~hz',1.0)
        self.rate = rospy.Rate(self.hz)
        self.minAngle = rospy.get_param('~minAngle',550)
        self.maxAngle = rospy.get_param('~maxAngle',2500)
        self.minPixel = rospy.get_param('~minPixel',0)
        self.maxPixel = rospy.get_param('~maxPixel',1280)

        self.updateInterpFunction()

        # Subs
        rospy.Subscriber('input',UInt16,self.setInput)
        rospy.Subscriber('setMinAngle',UInt16,self.setMinAngle)
        rospy.Subscriber('setMaxAngle',UInt16,self.setMaxAngle)

        # Pubs
        self.servoPub = rospy.Publisher('servo',UInt16,queue_size=10)

    def updateInterpFunction(self):
       xs = [self.minPixel,self.maxPixel]
       ys = [self.minAngle,self.maxAngle]
       self.interpFunc = interpolate.interp1d(xs,ys,bounds_error=False,fill_value=(self.minAngle,self.maxAngle))

    def setMinAngle(self,msg):
        self.minAngle = msg.data
        self.updateInterpFunction()

    def setMaxAngle(self,msg):
        self.maxAngle = msg.data
        self.updateInterpFunction()

    def setInput(self,msg):
        cmd = self.interpFunc(msg.data)
        self.servoPub.publish(cmd)

    def run(self):
        while not rospy.is_shutdown():
            self.rate.sleep()    

if __name__ == "__main__":
    node = image_transform()
    node.run()
