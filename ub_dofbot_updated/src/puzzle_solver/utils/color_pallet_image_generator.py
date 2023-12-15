import random
import cv2
import numpy as np


class image_generator:
    
    def rectangle_locations(self):
        start_points_x = [0,100,200,300,400] 
        start_points_y = [0,100,200,300,400]
        
        end_points_x = [100,200,300,400,500] 
        end_points_y = [100,200,300,400,500]
        
        start_points = []
        end_points = []
        
        for x in start_points_x:
            for y in start_points_y:
                start_points.append([x,y])
                
        for x in end_points_x:
            for y in end_points_y:
                end_points.append([x,y])
        
        return start_points, end_points
  

    def rowwise_patterns(self,puzzle_pattern, target_pattern):
        Actual_target_pattern = []
        Actual_target_pattern.append(target_pattern[0:3])
        Actual_target_pattern.append(target_pattern[5:8])
        Actual_target_pattern.append(target_pattern[10:13])
        Actual_target_pattern = np.transpose(Actual_target_pattern)
        
        Actual_puzzle_pattern = []
        Actual_puzzle_pattern.append(puzzle_pattern[0:5])
        Actual_puzzle_pattern.append(puzzle_pattern[5:10])
        Actual_puzzle_pattern.append(puzzle_pattern[10:15])
        Actual_puzzle_pattern.append(puzzle_pattern[15:20])
        Actual_puzzle_pattern.append(puzzle_pattern[20:])
        Actual_puzzle_pattern = np.transpose(Actual_puzzle_pattern)
        
        return Actual_puzzle_pattern,Actual_target_pattern


    def read_pattern(self,Blank):
        if Blank == True:
            color_pattern = ['R','G','B','Y','W','O',
                    'R','G','B','Y','W','O',
                    'R','G','B','Y','W','O',
                    'R','G','B','Y','W','O','0']
                    # 'R','G','B','Y','0']
        else:    
            color_pattern = ['R','G','B','Y','W','O',
                    'R','G','B','Y','W','O',
                    'R','G','B','Y','W','O',
                    'R','G','B','Y','W','O','O']
                    
        random.shuffle(color_pattern)
        random.shuffle(color_pattern)          
        return color_pattern
           

    def generate_image(self,color_pattern,size):
        rect_start_points, rect_end_points = self.rectangle_locations()
        Black = (0,0,0)        
        G = (0, 152, 37)
        B = (182, 34, 0)
        R = (0, 20, 200)
        Y = (1,203,231)
        W = (218,220,230)
        O = (0,151,225)
        
        
        pallet_width,pallet_height = 100,100
        
        canvas_width,canvas_height = pallet_width*size, pallet_height*size
        canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)
        canvas.fill(0)
        
        for i in range(25):
            color = color_pattern[i]            
            if color == 'R':
                pallet_color = R
            elif color == 'G':
                pallet_color = G
            elif color == 'B':
                pallet_color = B
            elif color == 'Y':
                pallet_color = Y
            elif color == 'W':
                pallet_color = W
            elif color == 'O':
                pallet_color = O
            elif color == '0':
                pallet_color = Black
            
            start_point = rect_start_points[i]
            end_point = rect_end_points[i]
            
            cv2.rectangle(canvas,start_point,end_point,pallet_color,-1)
            cv2.rectangle(canvas,start_point,end_point,Black,5)
        return canvas
        

    def generate_image_puzzle_pattern(self,puzzle_pattern,size):
        rect_start_points, rect_end_points = self.rectangle_locations()
        puzzle_pattern = np.transpose(puzzle_pattern)
        puzzle_pattern = [item for sublist in puzzle_pattern for item in sublist]
        
        Black = (0,0,0)
        
        G = (0, 152, 37)
        B = (182, 34, 0)
        R = (30, 30, 200)
        Y = (1,203,231)
        W = (218,220,230)
        O = (25,126,230)
        
        pallet_width,pallet_height = 100,100
        
        canvas_width,canvas_height = pallet_width*size, pallet_height*size
        canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)
        canvas.fill(0)
        
        for i in range(25):
            color = puzzle_pattern[i]            
            if color == 'R':
                pallet_color = R
            elif color == 'G':
                pallet_color = G
            elif color == 'B':
                pallet_color = B
            elif color == 'Y':
                pallet_color = Y
            elif color == 'W':
                pallet_color = W
            elif color == 'O':
                pallet_color = O
            elif color == '0':
                pallet_color = Black
            
            start_point = rect_start_points[i]
            end_point = rect_end_points[i]
            
            cv2.rectangle(canvas,start_point,end_point,pallet_color,-1)
            cv2.rectangle(canvas,start_point,end_point,Black,5)
        return canvas  
