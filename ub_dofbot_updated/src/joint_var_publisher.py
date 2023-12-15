#! /usr/bin/env python3

import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64MultiArray
import json
import time
import main
import tqdm

msg = Float64MultiArray()
err = 1 # th_1 adjusted by substracting 1


def solve_moves(feed_moves:int,joint_var:list):
    '''
    feed_moves : no. of moves per second
    '''
    
    rospy.loginfo("Solve_moves")
    rate = rospy.Rate(feed_moves)
   
    
    
    print("data_read")
    th5,th6 = 90.0,180.0
    print("publishing...")
    i = 0
    feed_time = 1000/feed_moves
    lenght_joint_var = len(joint_var)    
    # progress_bar = tqdm(total=lenght_joint_var, desc=("publishing.. "))
        
    while not rospy.is_shutdown() or i < lenght_joint_var:
        th1,th2,th3,th4 = joint_var[i]
        print(f"\t {i} / {lenght_joint_var}", end= '\r')
        if i ==0:
            msg.data = [90.0,90.0,90.0,90.0,th5,th6,1000]
            pub.publish(msg)
            i+=1
            
            rate.sleep()
            rate.sleep()
            rate.sleep()
            rospy.sleep(1)
            
            msg.data = [th1-err,th2,th3,th4,th5,th6,1000]
            pub.publish(msg)
            i+=1
            rate.sleep()
            rate.sleep()
            rate.sleep()
            rospy.sleep(1)
            # progress_bar.update(1)
        else:
            # msg.data = [th1,th2,th3,th4,th5,th6,feed_time*10]  
            msg.data = [th1-err,th2,th3,th4,th5,th6,feed_time*3]                      
            # msg.data = [th1-err,th2,th3,th4,th5,th6,feed_time]            
            pub.publish(msg)
            i+=1
            rate.sleep()
            # progress_bar.update(1)
        if i == lenght_joint_var:
            rospy.sleep(0.5)
            msg.data = [90.0, 90.0, 90.0, 0.0, th5, th6,1000]
            rate.sleep()
            rospy.sleep(1.2)
            msg.data = [90.0, 180.0, 0.0, 0.0, th5, th6,1000]
            pub.publish(msg)
            rate.sleep()
            rospy.sleep(1)
            # progress_bar.end()
        
    

    

    
if __name__ == "__main__":
    rospy.init_node('joint_var_node',anonymous=True)
    pub = rospy.Publisher('var_topic',Float64MultiArray, queue_size=10)
    
    try:  
        main.capture_solve_save(50,False)
        with open("src/database/joint_var.json",'r') as json_read:
            data = json.load(json_read)
        joint_var = data["joint_var_angles"]         
        print ("Sanket try successfully feed = 130 moves/sec for step size 2mm")
        print ("\nBest moves/sec found 30, for step size 5mm\n[step size = dist in detailed_path_generate function in main file]\n")
        # feed_moves  = int(input("Enter feed (no. of moves per second): ",)or "1") 
        feed_moves = int(30)
        rospy.sleep(2)
        solve_moves(feed_moves,joint_var)

    except:
        rospy.ROSInterruptException
        pass
        