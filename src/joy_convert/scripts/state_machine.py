#!/usr/bin/env python

import rospy
from std_msgs.msg import *

class state_machine(object):

    def __init__(self):

        rospy.init_node('state_machine')

        # Params
        self.hz = rospy.get_param('~hz',10.0)
        self.rate = rospy.Rate(self.hz)
        self.timeoutDuration = rospy.get_param('~timeoutDuration',5.0)

        self.yHomeVal = rospy.get_param('~y_home_val',1000)
        self.yPointVal = rospy.get_param('~y_point_val',1800)

        self.motionDetected = False
        self.lastMotionTs = None 

        # Subs
        rospy.Subscriber('x_in',UInt16,self.setX)
        rospy.Subscriber('set_y_home',UInt16,self.setYHome)
        rospy.Subscriber('set_y_point',UInt16,self.setYPoint)

        # Pubs
        self.yPub = rospy.Publisher('y_out',UInt16,queue_size=10)
        self.motionPub = rospy.Publisher('motionDetected',Bool,queue_size=10)
        self.eyePub = rospy.Publisher('eyeEnable',Bool,queue_size=10)
        self.soundPub = rospy.Publisher('soundEnable',Bool,queue_size=10)

    def setYHome(self,msg):
        self.yHomeVal = msg.data

    def setYPoint(self,msg):
        self.yPointVal = msg.data

    def setMotion(self,motion):
        if motion:
            self.lastMotionTs = rospy.get_time()
            if self.motionDetected is False:
                self.triggerSound()
                self.setEyes(True)
                self.yPub.publish(self.yPointVal)
            self.motionDetected = True
        else:
            self.motionDetected = False
            self.setEyes(False)
            self.yPub.publish(self.yHomeVal)

    def setEyes(self,val):
        self.eyePub.publish(val)

    def triggerSound(self):
        self.soundPub.publish(True)

    def setX(self,msg):
        self.setMotion(True)

    def run(self):
        while not rospy.is_shutdown():
            self.rate.sleep()
            if self.motionDetected is True:
                if rospy.get_time() - self.lastMotionTs > self.timeoutDuration:
                    self.setMotion(False)

            self.motionPub.publish(self.motionDetected)

if __name__ == "__main__":
    node = state_machine()
    node.run()
