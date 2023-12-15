#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def simple_publisher():
    rospy.init_node('simple_publisher', anonymous = True)
    
    pub = rospy.Publisher('my_topic',String,queue_size=10)
    
    rate = rospy.Rate(1)
    
    while not rospy.is_shutdown():
        message = "Hi"
        rospy.loginfo(message)
        pub.publish(message)
        rate.sleep()
        
if __name__ == '__main__':
    try:
        simple_publisher()
    except rospy.ROSInterruptException:
        pass