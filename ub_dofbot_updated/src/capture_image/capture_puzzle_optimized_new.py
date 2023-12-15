#! /usr/bin/env python
import cv2
import rospy
from Arm_Lib import Arm_Device
from std_msgs.msg import Float64MultiArray
import json
import random
import utils.color_pallet_image_generator as cpig
import subprocess
import time


CPIG = cpig.image_generator()
Arm = Arm_Device()
msg = Float64MultiArray()

class puzzle_capture:
    def read_target_from_user(self,autogenerate:bool):
        if not autogenerate:
            print("Enter target pattern")
            target_raw = ['0'] * 25
            seq = [0,5,10,1,6,11,2,7,12]
            for i in range(9):
                row = i//3 + 1
                col = i%3 + 1
                # my_str = "Row {0}, col {1} :".format(row)(col)
                ch = input("Row {0}, col {1}: ".format(row,col))
                CH = str(ch).upper()
                # print(ch)
                target_raw[seq[i]] = CH
                if (i+1)%3==0 and i != 0:
                    print()
            
        else:
            target_raw = ['R','G','B','Y','W','O',
                    'R','G','B','Y','W','O',
                    'R','G','B','Y','W','O',
                    'R','G','B','Y','W','O']
            random.shuffle(target_raw)
            random.shuffle(target_raw)
            target_raw.append('O')
            # target_raw = color_pattern[:9]
            
        return target_raw
            # pass
                    
            # rows = [raw_target[i:i+3] for i in range(0, len(raw_target),3)]
            # for row in rows:
            #     print(row)

    
    def save_puzzle(self,puzzle_pattern_raw,target_pattern_raw):
        # target_pattern = [target_pattern_raw[i:i+3] for i in range(0, len(target_pattern_raw),3)]
        
        target_row_1 = [target_pattern_raw[0], target_pattern_raw[5], target_pattern_raw[10]]
        target_row_2 = [target_pattern_raw[1], target_pattern_raw[6], target_pattern_raw[11]]
        target_row_3 = [target_pattern_raw[2], target_pattern_raw[7], target_pattern_raw[12]]
        
        target_pattern = [target_row_1,target_row_2,target_row_3]
        
        puzzle_pattern = [puzzle_pattern_raw[i:i+5] for i in range(0, len(puzzle_pattern_raw),5)]
        data={
            "puzzle_pattern":puzzle_pattern,
            "target_pattern":target_pattern,
            "raw_puzzle_pattern": puzzle_pattern_raw,
            "raw_target_pattern": target_pattern_raw
        }
        with open("src/database/patterns.json","w") as json_write:
            json.dump(data,json_write,indent=4)
        print("data saved to patterns.json")

        latest_puzzle = CPIG.generate_image_puzzle_pattern(puzzle_pattern,5)
        latest_target = CPIG.generate_image(target_pattern_raw,3)

        cv2.imwrite('src/database/puzzle.png',latest_puzzle)
        cv2.imwrite('src/database/target.png',latest_target)
        
    
    def camera_release(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Unable to open camera")
            
            command = 'fuser /dev/video0'
            print(command)
            process = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            stdout, stderr= process.communicate()
            print("std_out")
            pid = str(stdout.decode())
            print("process id : ",pid, " using camera")
            # print("\nstd_error")
            # print(stderr.decode())
            print('killing process ',pid)            
            command = 'kill -9'+pid
            print(command)
            process = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            stdout, stderr= process.communicate()
            print(stdout.decode())
            cap.release()
     
        
    def capture(self):
        cap = cv2.VideoCapture(0)
        # if not cap.isOpened():
        #     print("Error: Unable to open camera")
            
        #     command = 'fuser /dev/video0'
        #     print(command)
        #     process = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        #     stdout, stderr= process.communicate()
        #     print("std_out")
        #     pid = str(stdout.decode())
        #     print("process id : ",pid, " using camera")
        #     # print("\nstd_error")
        #     # print(stderr.decode())
        #     print('killing process ',pid)            
        #     command = 'kill -9'+pid
        #     print(command)
        #     process = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        #     stdout, stderr= process.communicate()
        #     print(stdout.decode())
        #     cap = cv2.VideoCapture(0)
        #     # free camera and call capture()
            

        ret,frame = cap.read()    
        if not ret:
            print("Error: Unable to capture")
            return
        cap.release()
        
        color_list, loc_list = self.color_extractor(frame)
        puzzle_pattern_raw = []
        for ind,clr in enumerate(color_list):
            center = (loc_list[ind][0],loc_list[ind][1])
            R,G,B = clr
            print(clr)
            
            if R<100 and B>100: #blue color
                current_color = 'B'
            elif R>253 and G>253 and B>240: # white
                current_color = 'W'
            elif R>253 and G>253 and B<220: # Yellow
                current_color = 'Y'
            elif R>253 and G>130 and B<200: # orange
                current_color = 'O'
            elif R>230 and G<130 and B<170: # red
                current_color = 'R'
            elif R<253 and G>135 and B<215: # green
                current_color = 'G'
            else:
                current_color = '0'
                
            # if R<100 and B>100: #blue color
            #     current_color = 'B'
            # elif R>253 and G>253 and B>240: # white
            #     current_color = 'W'
            # elif R>253 and G>253 and B<220: # Yellow
            #     current_color = 'Y'
            # elif R>253 and G>130 and B<200: # orange
            #     current_color = 'O'
            # elif R>253 and G<130 and B<170: # red
            #     current_color = 'R'
            # elif R<253 and G>135 and B<150: # green
            #     current_color = 'G'
            # else:
            #     current_color = '0'

            puzzle_pattern_raw.append(current_color)
            
        return puzzle_pattern_raw
       
        
    def color_extractor(self,image):
        list_loc = [(130,40), (230,40), (330,40), (430,40), (530,40),
                    (120,120),(225,120),(330,120),(435,120),(540,120),
                    (110,210),(220,210),(330,210),(440,210),(550,210),
                    (100,315),(215,315),(330,315),(445,315),(560,315),
                    (90,425),(210,425),(330,425),(450,425),(570,425)]
        color_list= []
        for loc in list_loc:
            y = loc[0]-10
            x = loc[1]-10
            r,g,b= 0,0,0
            for i in range(20):
                color = image[x][y]
                x = x+1
                y = y+1
                r += color[0]
                g += color[1]
                b += color[2]
            B = r//20
            G = g//20
            R = b//20
            color_list.append((R,G,B))
        return color_list, list_loc
    
       
CAP = puzzle_capture()


def main_capture():
    """
    best pose = 89,110,45,-45,90,180
    """
    Arm.Arm_serial_servo_write6(90.0,90.0,90.0,90.0,90.0,180.0,1500)
    rospy.sleep(2)
    Arm.Arm_serial_servo_write6(89.0,110.0,45.0,-45.0,90.0,180.0,1500)
    rospy.sleep(2)
    CAP.camera_release()
    puzzle_pattern_raw = CAP.capture()
    print("puzzle_pattern_raw :\n",puzzle_pattern_raw)
    # target_pattern_raw= CAP.read_target_from_user(True)
    
    Autogenerate = (input("\ndo you want to auto generate target pattern? \n'y' or 'n' : "))
    # Autogenerate = 'y'
    if Autogenerate == 'y':
        target_pattern_raw= CAP.read_target_from_user(True)
    elif Autogenerate == 'n':
        target_pattern_raw= CAP.read_target_from_user(False)
    CAP.save_puzzle(puzzle_pattern_raw,target_pattern_raw)

main_capture()