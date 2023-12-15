#! /usr/bin/env python3
import rospy
from std_msgs.msg import Float64MultiArray
from Arm_Lib import Arm_Device
Arm = Arm_Device()



def callback(data):
    rospy.loginfo("Received_data: %s", str(data.data))
    # rospy.loginfo(ArmStart)
    angles = (data.data)
    th_1 = float(angles[0])
    th_2 = float(angles[1])
    th_3 = float(angles[2])
    th_4 = float(angles[3])
    th_5 = float(angles[4])
    th_6 = float(angles[5])
    dtime = int(angles[6])
    # move(th_1, th_2, th_3,th_4,th_5,th_6,dtime)
    # if ArmStart == 'y' or ArmStart == 'Y':
        # Arm.Arm_serial_servo_write6(th_1, th_2, th_3,th_4,th_5,th_6,dtime)
    Arm.Arm_serial_servo_write6(th_1, th_2, th_3,th_4,th_5,th_6,dtime)
        
# def move(th_1, th_2, th_3,th_4,th_5,th_6,dtime):
    
   
    

if __name__=='__main__':
    
    # ArmStart = str(input("Do you want to start movemets? y or n :",))
    # if ArmStart == 'y':
    #     rospy.loginfo('Arm moving')
    # else:
    #     rospy.loginfo('Arm set off')
    rospy.loginfo("Subscriber_is_running")
    rospy.init_node('Joint_variable_subscriber',anonymous=True)
    rospy.Subscriber('var_topic',Float64MultiArray,callback)
    rospy.spin()
    
    