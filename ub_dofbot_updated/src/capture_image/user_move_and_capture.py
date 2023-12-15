#! /usr/bin/env python
import cv2
import rospy
from Arm_Lib import Arm_Device
from std_msgs.msg import Float64MultiArray
import json
import time
import numpy as np

Arm = Arm_Device()
msg = Float64MultiArray()


def capture():
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Unable to open camera")
            return

        ret,frame = cap.read()    
        if not ret:
            print("Error: Unable to capture")
            return
        cap.release()
        return frame

def transform_home(frame):
    source_pts = np.float32([[67,35], [530,0], [50,479], [625,455]])
    destination = np.float32([[0,0], [640,0], [0,480], [640,480]])
    mat = cv2.getPerspectiveTransform(source_pts,destination)
    result = cv2.warpPerspective(frame, mat, (640,480))
    return result

def transform_1(frame):    
    source_pts = np.float32([[65,0], [585,0], [40,480], [640,480]])
    destination = np.float32([[0,0], [640,0], [0,480], [640,480]])
    mat = cv2.getPerspectiveTransform(source_pts,destination)
    result = cv2.warpPerspective(frame, mat, (640,480))
    return result

def user(user_array):    
    Arm.Arm_serial_servo_write6(user_array[0], user_array[1], user_array[2], user_array[3], 90.0, 180.0, 100)
    frame = capture()
    # cv2.imshow("frame_", frame)
    # cv2.imshow('tran',transform_home(frame))
    # cv2.imshow('tran',transform_1(frame))
    
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    

def color_extract():
    user([87,110,45,-45])
    frame = capture()
    transform_img = transform_home(frame)
    user([89,90,58,-45])
    frame = capture()
    transform_img_1 = transform_1(frame)
    
    
    for row in range(0,641,158):        
        for col in range(0, 481,115):
            center = (row,col)
            clr = (0, 0,0)
            radius = 20
            
            roi = transform_img[col:col+10, row:row+10]
            avg_clr = np.mean(roi, axis=(0,1))
            avg_clr_int = np.round(avg_clr).astype(int)
            # clr_tupple = (avg_clr_int[0], avg_clr_int[1], avg_clr_int[2])
            # clr_tupple = tuple(avg_clr_int)
            
            cv2.circle(transform_img,center,radius-3,avg_clr_int, -1)
            print(avg_clr_int)

            roi = transform_img_1[col:col+10, row:row+10]
            avg_clr = np.mean(roi,axis=(0,1))
            avg_clr_int = np.round(avg_clr).astype(int)
            # clr_tupple = (avg_clr_int[0], avg_clr_int[1], avg_clr_int[2])
            clr_tupple = tuple(avg_clr_int)
            
            # cv2.circle(transform_img_1,center,radius-3,clr_tupple, -1)
            # print(avg_clr_int)
            # print("clr_tupple: ",clr_tupple)
            
            
            # cv2.circle(transform_img,center,radius,clr, -1)
            # cv2.circle(transform_img_1,center,radius,clr, -1)
            print()
        print()
            
    
    
    
    
    cv2.imshow('tran',transform_img)
    cv2.imshow('tran1',transform_img_1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    pass



color_extract()


"""
while(True):
    user_input = input("Enter Joint vars: ")
    # # 89.0,110.0,45.0,-45.0,90.0,180.0,2000
    string_numbers = user_input.split()
    user_array = [float(num) for num in string_numbers]
    
    user(user_array)
    '''
    
    Arm.Arm_serial_servo_write6(105, 70, 40, 0, 90.0, 180.0, 1500)
    time.sleep(1.5)
    th4_ref = 0
    for j in range(4):
        
        th4 = th4_ref - (j*10)
        th1 = 105
        for i in range(4):
            th1 -= i*(5)
            fname = "new_images/"
            fname += str(j)+str(i)
            fname += ".png"
            user_array = [th1, 70, 40, th4]
            user(user_array)
            time.sleep(0.1)
            frame = capture()
            cv2.imshow(fname, frame)
            # cv2.imwrite(fname,frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    '''
    # cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
    # get 2 frames and apply filter on them.
    
"""