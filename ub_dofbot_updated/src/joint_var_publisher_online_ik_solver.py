#! /usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64MultiArray
import json                                   
import my_inverse_kinematics.main_inv_kin as IK
import utils.inv_kin_functions as IKF

msg = Float64MultiArray()



def solve_moves(feed_moves:int,final_path_co_ords:list):
    '''
    feed_moves : no. of moves per second
    '''
    # feed_moves = 1 # no. of moves per second
    # rospy.init_node('joint_var_node',anonymous=True)
    # pub = rospy.Publisher('var_topic',Float64MultiArray, queue_size=10)
    
    
    with open("src/database/dofbot_details.json","r") as json_read:
        data = json.load(json_read)

    l1,l2,l3,l4,finger_len,circum_points = data['l1'],data['l2'],data['l3'],data['l4'],data['finger_len'],data['circum_points']

    l4 += finger_len
    
    
    
    
    rospy.loginfo("Solve_moves")
    rate = rospy.Rate(feed_moves)
    
    print("data_read")
    th5,th6 = 90.0,180.0
    print("publishing...")
    # rospy.loginfo("publishing...")
    i = 0
    feed_time = 1000/feed_moves
    # lenght_joint_var = len(joint_var)    
    # th1,th2,th3,th4 = joint_var[0]
    # msg.data = [th1,th2,th3,th4,th5,th6,2000]
    # pub.publish(msg)
    # rospy.sleep(5)
    
    lenght_joint_var = len(final_path_co_ords)
    while not rospy.is_shutdown() or i < lenght_joint_var:
        # print("inside while")
        # var_data = joint_var[i]
        # th1,th2,th3,th4 = joint_var[i]
        # rospy.loginfo(i)
        # msg.data = [th1,th2,th3,th4,th5,th6,feed_time]
        # pub.publish(msg)
        # i+=1
        # rate.sleep()
        pt = final_path_co_ords[i]
        
                    
        th_1,th_2,th_3,th_4,J1_pt,J2_pt,J3_pt,J4_pt = IKF.joint_variables(pt,l1,l2,l3,l4,circum_points)
        if i == 0:
            
            msg.data = [90.0,90.0,90.0,90.0,th5,th6,3000]
            pub.publish(msg)
            i+=1
            
            rate.sleep()
            rate.sleep()
            rate.sleep()
            rospy.sleep(3)
            
            msg.data = [th_1,th_2,th_3,th_4,th5,th6,3000]
            pub.publish(msg)
            i+=1
            rate.sleep()
            rate.sleep()
            rate.sleep()
            rospy.sleep(3)
            
            
        else:
            msg.data = [th_1,th_2,th_3,th_4,th5,th6,feed_time*10]
            # msg.data = [th_1,th_2,th_3,th_4,th5,th6,feed_time]
            
            pub.publish(msg)
            i+=1
            rate.sleep()
            
        # pub.publish(msg)
        # i+=1
        # rate.sleep()



if __name__ == "__main__":
    rospy.init_node('joint_var_node',anonymous=True)
    pub = rospy.Publisher('var_topic',Float64MultiArray, queue_size=10)
    
    
    try:        
        with open("src/database/detailed_final_path.json",'r') as json_read:
            data = json.load(json_read)
        final_path_co_ords = data["final_path"]        
        feed_moves  = int(input("Enter feed (no. of moves per second): ",)or "1") 
        
        # loc1 = joint_var[0]
        # th1,th2,th3,th4 = loc1
        # th5,th6 = 90.0,180.0
        # msg.data = [th1,th2,th3,th4,th5,th6,5000]
        # pub.publish(msg)
        
        
        solve_moves(feed_moves,final_path_co_ords)
    except:
        rospy.ROSInterruptException
        pass
        