#! /usr/bin/env python

import utils.inv_kin_functions as IK
import json
from Arm_Lib import Arm_Device
from std_msgs.msg import Float64MultiArray

Arm = Arm_Device()
msg = Float64MultiArray()

def move_to_point(P:list):
    with open("src/database/dofbot_details.json","r") as json_read:
        data = json.load(json_read)

    l1,l2,l3,l4,finger_len,circum_points = data['l1'],data['l2'],data['l3'],data['l4'],data['finger_len'],data['circum_points']
    l4 += finger_len
    
    th_1,th_2,th_3,th_4,J1_pt,J2_pt,J3_pt,J4_pt = IK.joint_variables(P,l1,l2,l3,l4,circum_points)
    # Arm.Arm_serial_set_torque(1)
    
    Arm.Arm_serial_servo_write6(th_1, th_2, th_3, th_4, 90.0, 180.0, 1000)
    
while True:
    user_input = input("Enter 3d point: ")
    string_numbers = user_input.split()
    P = [float(num) for num in string_numbers]
    move_to_point(P)