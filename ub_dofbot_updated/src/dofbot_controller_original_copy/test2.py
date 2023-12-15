#! /usr/bin/env python

import rospy

if __name__ == "__main__":
    rospy.init_node("test_node_3")
    rospy.loginfo("Hi_from_3rd node")
    rate = rospy.Rate(2)

    while not rospy.is_shutdown():
        rospy.loginfo("hello")
        rate.sleep()