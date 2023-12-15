#! /usr/bin/env python
import cv2
import rospy
from Arm_Lib import Arm_Device
from std_msgs.msg import Float64MultiArray
import json

Arm = Arm_Device()
msg = Float64MultiArray()

class puzzle_capture:
    def capture_target(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Unable to open camera")
            return

        ret,frame = cap.read()    
        if not ret:
            print("Error: Unable to capture")
            return
        cap.release()
        
        frameG = cv2.GaussianBlur(frame,(15,15),2)
        frameGS = cv2.addWeighted(frame,2,frameG,-1,1)

        
        # color_list, loc_list = self.color_extractor_target(frame)
        color_list, loc_list = self.color_extractor_target(frameGS)
        
        
        for ind,clr in enumerate(color_list):
            # color = (0,0,0) #BGR
            center = (loc_list[ind][0],loc_list[ind][1])
            cv2.circle(frameGS,center,11,(255,0,0),2)
            R,G,B = clr
            
            if R>220 and G<155 and B<170: # red
                current_color = 'R'
                color = (0,0,255)
            elif R>220 and G>155                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       and B<200: # orange
                current_color = 'O'
                color = (51,153,255)
            elif R>220 and G>253 and B>240: # white
                current_color = 'W'
                color = (255,255,255)
            elif R>220 and G>253 and B<220: # Yellow
                current_color = 'Y'
                color = (0,204,204)  
            
           
            elif R<253 and G>135 and B<150: # green
                current_color = 'G'
                color = (0,255,0)
            elif R<100 and B>100: #blue color
                current_color = 'B'
                color = (255,0,0)
            
            else:
                current_color = '0'
                color = (0,0,0)
                
                    
            cv2.circle(frameGS,center,10,color,-1) 
            # print(clr,loc_list[ind],", ", current_color)
            print(current_color," ",clr)
            if ind != 0 and (ind+1)%3==0:
                print()
        # frameM = cv2.medianBlur(frame,25)
        cv2.imshow('frame',frame)
        # cv2.imshow('frame_M',frameM)
        cv2.imshow('frame_G',frameG)
        cv2.imshow('3',frameGS)
    
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    
    def capture(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Unable to open camera")
            return

        ret,frame = cap.read()    
        if not ret:
            print("Error: Unable to capture")
            return
        cap.release()
        
        color_list, loc_list = self.color_extractor(frame)
        
        
        
        
        for ind,clr in enumerate(color_list):
            # color = (0,0,0) #BGR
            center = (loc_list[ind][0],loc_list[ind][1])
            cv2.circle(frame,center,11,(255,0,0),2)
            
            R,G,B = clr
            if R<100 and B>100: #blue color
                current_color = 'B'
                color = (255,0,0)
            elif R>253 and G>253 and B>240: # white
                current_color = 'W'
                color = (255,255,255)
            elif R>253 and G>253 and B<220: # Yellow
                current_color = 'Y'
                color = (0,204,204)  
            elif R>253 and G>130 and B<200: # orange
                current_color = 'O'
                color = (51,153,255)
            elif R>253 and G<130 and B<170: # red
                current_color = 'R'
                color = (0,0,255)
            elif R<253 and G>135 and B<150: # green
                current_color = 'G'
                color = (0,255,0)
            else:
                current_color = '0'
                color = (0,0,0)
                
                    
            cv2.circle(frame,center,10,color,-1) 
            # print(clr,loc_list[ind],", ", current_color)
            # print(current_color)
            
            print(clr)
            
            if ind != 0 and (ind+1)%5==0:
                print()
            
        cv2.imshow('frame',frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return color_list,loc_list
     
    
    def capture_1(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Unable to open camera")
            return

        ret,frame = cap.read()    
        if not ret:
            print("Error: Unable to capture")
            return
        cap.release()
        
        color_list, loc_list = self.color_extractor_1(frame)
        
        for ind,clr in enumerate(color_list):
            # color = (0,0,0) #BGR
            center = (loc_list[ind][0],loc_list[ind][1])
            cv2.circle(frame,center,11,(255,0,0),2)
            
            R,G,B = clr
            if R<100 and B>100: #blue color
                current_color = 'B'
                color = (255,0,0)
            elif R>253 and G>253 and B>240: # white
                current_color = 'W'
                color = (255,255,255)
            elif R>253 and G>253 and B<220: # Yellow
                current_color = 'Y'
                color = (0,204,204)  
            elif R>253 and G>130 and B<200: # orange
                current_color = 'O'
                color = (51,153,255)
            elif R>253 and G<130 and B<170: # red
                current_color = 'R'
                color = (0,0,255)
            elif R<253 and G>135 and B<150: # green
                current_color = 'G'
                color = (0,255,0)
            else:
                current_color = '0'
                color = (0,0,0)
                
                    
            cv2.circle(frame,center,10,color,-1) 
            # print(clr,loc_list[ind],", ", current_color)
            # print(current_color)
            
            print(clr)
            
            if ind != 0 and (ind+1)%5==0:
                print()
            
        cv2.imshow('frame',frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        return color_list,loc_list
    
    
      
    def color_extractor_target(self,image):
        list_loc = [(185,205), (260,140), (326,80),
                    (250,281),(320,215),(395,153),
                    (312,345),(390,285),(455,215)]
        
        color_list= []
        for loc in list_loc:
            y = loc[0]-7
            x = loc[1]-7
            r,g,b= 0,0,0
            for i in range(14):
                color = image[x][y]
                x = x+1
                y = y+1
                r += color[0]
                g += color[1]
                b += color[2]
            B = r//14
            G = g//14
            R = b//14
            color_list.append((R,G,B))
            
            
        return color_list, list_loc
    
        
    def color_extractor(self,image):
        list_loc = [(120,40), (230,15), (330,15), (430,15), (530,15),
                    (120,120),(225,120),(330,120),(435,120),(540,120),
                    (110,210),(220,210),(330,210),(440,210),(550,210),
                    (100,315),(215,315),(330,315),(445,315),(560,315),
                    (90,425),(210,425),(330,425),(450,425),(570,425)]
        color_list= []
        for loc in list_loc:
            y = loc[0]-10
            x = loc[1]-10
            # r,g,b= 0,0,0
            B,G,R = 255,255,255
            for i in range(20):
                color = image[x][y]
                x = x+1
                y = y+1
                
                if color[0]<B:
                    B=color[0]
                if color[1]<G:
                    G = color[1]
                if color[2]<R:
                    R = color[2]
                
            #     r += color[0]
            #     g += color[1]
            #     b += color[2]
            # B = r//20
            # G = g//20
            # R = b//20
            
            
            color_list.append((R,G,B))
        return color_list, list_loc
        
        
    def color_extractor_1(self,image):
        list_loc = [(70,30), (180,15), (290,15), (430,15), (530,15),
                    (60,120),(180,120),(300,120),(435,100),(540,96),
                    (60,240),(180,230),(300,230),(440,210),(550,210),
                    (60,370),(190,360),(314,350),(450,340),(580,340),
                    (70,465),(180,465),(330,465),(450,465),(570,465)]
        color_list= []
        for loc in list_loc:
            y = loc[0]-10
            x = loc[1]-10
            # r,g,b= 0,0,0
            B,G,R = 255,255,255
            for i in range(20):
                color = image[x][y]
                x = x+1
                y = y+1
                
                if color[0]<B:
                    B=color[0]
                if color[1]<G:
                    G = color[1]
                if color[2]<R:
                    R = color[2]
                
                # r += color[0]
                # g += color[1]
                # b += color[2]
            # B = r//20
            # G = g//20
            # R = b//20
            
            
            color_list.append((R,G,B))
        return color_list, list_loc    
    
    
        
CAP = puzzle_capture()


def main_capture():
    """
    best pose = 89,110,45,-45,90,180
    """
    Arm.Arm_serial_servo_write6(89.0,110.0,45.0,-45.0,90.0,180.0,1000)
    # Arm.Arm_serial_servo_write6(48.0,70.0,30.0,-10.0,90.0,180.0,2000)
    rospy.sleep(1)
    color_list,loc_list = CAP.capture()
    
    # clr_list, = CAP.capture()
    # CAP.capture_target()
    
    print("----------------------")
    
    Arm.Arm_serial_servo_write6(87.0,90.0,58.0,-45.0,90.0,180.0,1000)
    rospy.sleep(1)
    # clr_list_1 = CAP.capture_1()
    color_list_1,loc_list_1 = CAP.capture_1()
    
    color_difs= []
    for i in range(2):
        for j in range (25):
            B,G,R = color_list[j]
            # clr = color_list[j]
            clr_1 = color_list_1[j]
            
            if B > clr_1[0]:
                B = clr_1[0]
            if G > clr_1[1]:
                G = clr_1[1]
            if R > clr_1[2]:
                R = clr_1
            
            color_difs.append([B,G,R]) 

    color_ref = []
    
    # RED
    b,g,r = 255,255,255
    for i in range(4):
        clr = color_difs[i]
        if clr[0]<b:
            b = clr[1]
        if clr[1]<g:
            g = clr[1]
        if clr[2]<r:
            r = clr[2]
        color_ref.append([b,g,r])
    
    # BLUE
    b,g,r = 255,255,255
    for i in range(5,9):
        clr = color_difs[i]
        if clr[0]<b:
            b = clr[1]
        if clr[1]<g:
            g = clr[1]
        if clr[2]<r:
            r = clr[2]
        color_ref.append([b,g,r])
        
     # YELLOW
    b,g,r = 255,255,255
    for i in range(10,14):
        clr = color_difs[i]
        if clr[0]<b:
            b = clr[1]
        if clr[1]<g:
            g = clr[1]
        if clr[2]<r:
            r = clr[2]
        color_ref.append([b,g,r])

    # GREEN
    b,g,r = 255,255,255
    for i in range(15,19):
        clr = color_difs[i]
        if clr[0]<b:
            b = clr[1]
        if clr[1]<g:
            g = clr[1]
        if clr[2]<r:
            r = clr[2]
        color_ref.append([b,g,r])

    # WHITE
    b,g,r = 255,255,255
    for i in range(20,24):
        clr = color_difs[i]
        if clr[0]<b:
            b = clr[1]
        if clr[1]<g:
            g = clr[1]
        if clr[2]<r:
            r = clr[2]
        color_ref.append([b,g,r])
        
    # Orange
    b,g,r = 255,255,255
    for i in range(25):
        if (i+1)%5 ==0:
            clr = color_difs[i]
            if clr[0]<b:
                b = clr[1]
            if clr[1]<g:
                g = clr[1]
            if clr[2]<r:
                r = clr[2]
            color_ref.append([b,g,r])

    # add blank space:
    color_ref.append(color_difs[24])
    
    print()
    print()
    
    print("color ref:")
    for ref in color_ref:
        print(ref)
        
    
    
    
main_capture()

# if __name__=="__main__":
#     rospy.init_node('capture_image')
#     rate = rospy.Rate(1)
#     try:
#         main_capture(True)
#         # capture_pose()
#         # capture_and_save()
        
#     except rospy.ROSInterruptException:
#         pass