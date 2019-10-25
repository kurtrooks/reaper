#!/usr/bin/env python

import os
import rospy
from std_msgs.msg import *

class pipe_reader(object):

    def __init__(self):
        rospy.init_node('pipe_reader')
        self.hz = rospy.get_param('~hz',20.0)
        self.pipeName = rospy.get_param('~pipe_name','/tmp/xy')

        self.xPub = rospy.Publisher('x',UInt16,queue_size=10)
        self.yPub = rospy.Publisher('y',UInt16,queue_size=10)
        
        self.fifo = None
        self.openPipe(self.pipeName)
        self.rate = rospy.Rate(self.hz)
        
    def openPipe(self,name):
        try:
            os.mkfifo(name)
        except Exception as ex:
            print ex

        self.fifo = open(name)

    def run(self):
        while not rospy.is_shutdown():
            self.rate.sleep()
            if self.fifo is not None:
                data = self.fifo.read()
                if len(data) > 0:
                    sdata = data.split()
                    x = int(sdata[0])
                    y = int(sdata[1])
                    self.xPub.publish(x)
                    self.yPub.publish(y)
            
if __name__ == "__main__":
    node = pipe_reader()
    node.run()
