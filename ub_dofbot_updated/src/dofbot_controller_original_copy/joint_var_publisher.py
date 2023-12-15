#! /usr/bin/env python

import rospy
from std_msgs.msg import Float64MultiArray
import inverse_kinematics.Inv_kin_1 as IK


def callback(data):
    P = list(data.data)
    print('\nP:',P)
    
    dtime = int(P[3])
    P_ik = P[0:3] # slicing to get x,y,z point to find joint variables
    # print('newP:',P)
    th_1,th_2,th_3,th_4 = IK.ik(P_ik)
    # print(th_1,th_2,th_3,th_4)
    
    th_1 = round(float(th_1),2)
    th_2 = round(float(th_2),2)
    th_3 = round(float(th_3),2)
    th_4 = round(float(th_4),2)
    
    th_5 = float(P[4])
    th_6 = float(P[5])
    
    msg.data = [th_1,th_2,th_3,th_4,th_5,th_6,dtime]
    # print('msg: {msg} \n')
    # print('msg:', msg,'\n')
    pub.publish(msg)
    pass

if __name__ == '__main__':
    rospy.init_node('Joint_variable_publisher',anonymous=True)
    
    msg = Float64MultiArray()
    sub = rospy.Subscriber('target_pt_3d',Float64MultiArray,callback)
    pub = rospy.Publisher('Joint_variables', Float64MultiArray, queue_size=10)
    
    
    th_5 = 90.0
    th_6 = 180.0
    dtime = 500
    print('dtime: ', dtime)
    rospy.spin()
    