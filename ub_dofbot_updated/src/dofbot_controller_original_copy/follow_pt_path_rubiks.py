#! /usr/bin/env python

import rospy
from std_msgs.msg import Float64MultiArray
import json

dist = 5  # distance between two consecutive points in mm
z_safe = 35
z_touch = 10
    
    
if __name__ == '__main__':
    rospy.init_node('target_pt_3d_publisher')
    pub = rospy.Publisher('target_pt_3d', Float64MultiArray, queue_size=10)
    msg = Float64MultiArray()
    feed_rate = 2 # time in seconds to perform specific task
    
    with open("/src/database/detailed_final_path.json", "r") as json_file:
        data = json.load(json_file)
    
    p_list = data["final_path"]
    


while not rospy.is_shutdown():
    for pt in p_list:
        x = pt[0]
        y = pt[1]
        z = pt[2]
        
        dtime = int(feed_rate/1000)
        th_5 = 90.0
        th_6 = 180.0
        msg.data = [x,y,z,dtime,th_5,th_6]
        pub.publish(msg)
        rate = rospy.Rate(10) # rospy.Rate(__number of messages per second__)
        rate.sleep()