import numpy as np
import math


class Inverse_kinematics_solver:
    def __init__(self) -> None:
        
        pass


    def th_1(self,P):
        """
        Input: P = (x,y,z)
        Output: th_1
        """
        x,y,z = P[0], P[1], P[2]
        if x != 0:
            theta_1 = np.arctan(y/x)
        else:
            theta_1 = np.deg2rad(90)
        theta_1 = np.rad2deg(theta_1)
        if(theta_1 < 0):
                theta_1 = round(180 + theta_1,2)
        return theta_1


    def new_2d_cords(self,P:list):
        X,Y,Z = P[0],P[1],P[2]
        x = np.sqrt(X**2 + Y**2)
        y = Z
        p = (round(x,2),round(y,2))
        return p


    def pts_on_circum(self, p,num_points,l1,l2,l3,l4):
        center_x = p[0]
        center_y = p[1]
        alpha = 360/num_points
        points = []
        J2 = [0,l1]
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            x = center_x + l4 * math.cos(angle)
            y = center_y + l4 * math.sin(angle)
            dist_from_J2 = np.sqrt(((x-J2[0])**2)+((y-J2[1])**2))
            if dist_from_J2<(l2+l3) and dist_from_J2>(np.sqrt(2)*(l2)) and x >= 0 and y>=0:
                
                #===========================================
                J1_pt = [0,l1]
                J3_pt = (round(x,2),round(y,2))
                D = dist_from_J2
                J4_pt = p
                
                th_2,th_3  = self.thetas(J1_pt,J3_pt,l2,D)
                lamda = abs(np.rad2deg(np.arctan2((J4_pt[1]-J3_pt[1]),(J4_pt[0]-J3_pt[0]))))
                th_4 = 90 - (lamda+(th_3+th_2-90))
                theta = th_3+th_2-90
                theta_lamda = theta+lamda
                th_4 = round(90 - theta_lamda,2)
                
                #===========================================
                if th_4>=0 and th_2>=0 and th_3>=0:
                    points.append([x, y])
                    break
        return th_2,th_3,th_4,J3_pt,J4_pt


    def thetas(self, J1_pt,J3_pt,l2,D):
        beta = np.rad2deg(np.arctan2((J3_pt[1] - J1_pt[1]),(J3_pt[0] - J1_pt[0])))
        alpha = np.rad2deg(np.arccos((D/2)/l2))
        th_2 = round((beta + alpha),2)
        phi = 180-(2*alpha)
        th_3 = round(phi - 90,2)
        return th_2,th_3


    def J2_pt(self, l2,th_2,J1_pt):
        x = (l2 * np.cos(np.deg2rad(th_2)))+J1_pt[0]
        y = (l2 * np.sin(np.deg2rad(th_2)))+J1_pt[1]
        J2_point = (round(x,2),round(y,2))
        return J2_point
    

    def convert_2d_to_3d(self,pt:list,th1:float)->tuple:
        x,y = pt
        Z = y
        Y = round(np.sin(np.deg2rad(th1))*x,2)
        X = round(np.cos(np.deg2rad(th1))*x,2)
        return(X,Y,Z)



IK = Inverse_kinematics_solver()


def joint_variables(P:list,l1:int,l2:int,l3:int,l4:int,tot_circum_points:int)->tuple:
    """
    input : P [x,y,z]
            dofbot details = l1, l2, l3, l4
            total_circum_points : default = 1999, high number result in high accuracy and high computation.
    Output:
            Joint Variables = th1, th2, th3, th4
            Joint variable location 2d = J1_pt, J2_pt, J3_pt, J4_pt
    """
    th_1 = round(IK.th_1(P),2)
    p = IK.new_2d_cords(P)
    th_2,th_3,th_4,J3_pt,J4_pt = IK.pts_on_circum(p,tot_circum_points,l1,l2,l3,l4)   
    J1_pt = (0,l1)
    J2_pt = IK.J2_pt(l2,th_2,J1_pt)
    
    #convet_2d to 3d points
    J1_pt = IK.convert_2d_to_3d(J1_pt,th_1)
    J2_pt = IK.convert_2d_to_3d(J2_pt,th_1)
    J3_pt = IK.convert_2d_to_3d(J3_pt,th_1)
    J4_pt = IK.convert_2d_to_3d(J4_pt,th_1)
    
    # return round(th_1,2),round(th_2,2),round(th_3,2),round(th_4,2),round(J1_pt,2),round(J2_pt,2),round(J3_pt,2),round(J4_pt,2)
    return th_1,th_2,th_3,th_4,J1_pt,J2_pt,J3_pt,J4_pt


# # Function cross-checking
# print(joint_variables([100,100,100],119,87,87,119,1999)) # <-for testing
# P = [0,0,0]
# print(P)
# th1 = IK.th_1(P)
# print(th1)
# p = (IK.new_2d_cords(P))
# print(p)
# IK.convert_2d_to_3d(p,th1)