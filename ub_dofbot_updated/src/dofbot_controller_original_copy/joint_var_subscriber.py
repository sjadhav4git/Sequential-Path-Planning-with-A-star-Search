#! /usr/bin/env python
import rospy
from std_msgs.msg import Float64MultiArray
from Arm_Lib import Arm_Device
import time

th_1 = 90.0
th_2 = 90.0
th_3 = 90.0
th_4 = 90.0
th_5 = 90.0
th_6 = 90.0
dtime = 1000

def callback(data):
    rospy.loginfo("Received_data: %s", str(data.data))
    angles = (data.data)
    th_1 = float(angles[0])
    th_2 = float(angles[1])
    th_3 = float(angles[2])
    th_4 = float(angles[3])
    th_5 = float(angles[4])
    th_6 = float(angles[5])
    dtime = int(angles[6])
    move(th_1, th_2, th_3,th_4,th_5,th_6,dtime)
    
    pass

def move(th_1, th_2, th_3,th_4,th_5,th_6,dtime):
    Arm = Arm_Device()
    Arm.Arm_serial_servo_write6(th_1, th_2, th_3,th_4,th_5,th_6,dtime)

    
    

def listener():
    rospy.init_node('Joint_variable_subscriber',anonymous=True)
    rospy.Subscriber('Joint_variables',Float64MultiArray,callback)
    rospy.spin()
    

if __name__ == '__main__':
    listener()
    
