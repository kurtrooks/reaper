#!/usr/bin/env python

import rospy
from std_msgs.msg import *

class state_machine(object):

    def __init__(self):
        rospy.init_node('state_machine')
        self.hz = rospy.get_param('~hz',10.0)
        self.rate = rospy.Rate(self.hz)
        self.timeoutVal = rospy.get_param('~timeoutDuration',5.0)
        self.timeoutDuration = rospy.Duration(self.timeoutVal)

        self.motionDetected = False
        self.lastMotionTs = None 

        rospy.Subscriber('x_in',UInt16,self.setX)
        rospy.Subscriber('y_in',UInt16,self.setY)

        self.xPub = rospy.Publisher('x_out',UInt16,queue_size=10)
        self.yPub = rospy.Publisher('y_out',UInt16,queue_size=10)

        self.motionPub = rospy.Publisher('motionDetected',Bool,queue_size=10)
        self.eyePub = rospy.Publisher('eyeEnable',Bool,queue_size=10)
        self.soundPub = rospy.Publisher('soundEnable',Bool,queue_size=10)

    def setMotion(self,motion):
        if motion:
            self.lastMotionTs = rospy.get_time()
            if self.motionDetected is False:
                self.triggerSound()
                self.setEyes(True))
            self.motionDetected = True
        else:
            self.motionDetected = False
            self.setEyes(False)

    def setEyes(self,val):
        self.eyePub.publish(val)

    def triggerSound(self):
        self.soundPub.publish(True)

    def setX(self,msg):
        self.setMotion(True)
        self.xPub.publish(msg)

    def setY(self,msg):
        self.setMotion(True)
        self.yPub.publish(msg)

    def run(self):
        while not rospy.is_shutdown():
            self.rate.sleep()
            if self.motionDetected is True:
                if rospy.get_time() - self.lastMotionTs > self.timeoutDuration:
                    self.setMotion(False)

if __name__ == "__main__":
    node = state_machine()
    node.run()
