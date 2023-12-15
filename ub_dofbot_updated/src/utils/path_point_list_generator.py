#! /usr/bin/env python
#####################################################################################
#
#    Function: line_point
#    Input   : two_points,d
#              d = Distance between any two consecutive point = 2 mm
#    Output  : List of all points on the line marked points received from input

#    Function: tot_point_list_generate
#    Input   : list of points,d
#    Output  : List of all points to travel by end effector
#    
#####################################################################################

import numpy as np

def line_points(point1,point2,d):
    ponit1 = np.array(point1)
    point2 = np.array(point2)
    distance = np.sqrt(np.sum((point2-ponit1)**2))
    # print('Distance :', distance)
    if distance >2:
        if int(distance)%2 == 0:
            n = int(distance/d) + 1
        else:
            n = int(distance/d) + 2
    elif distance <=2:
        n = 2

    t = np.linspace(0,1, num=n)
    line_points = (ponit1 + t[:,np.newaxis]*(point2 - ponit1))
    return (line_points)


# end_point_list = [[0,0,0],[10,10,10],[20,10,10],[20,20,10],[10,20,10],[10,10,10]]

def tot_point_list_generate(end_point_list,d):
    tot_pt_list = []
    for i in range(len(end_point_list)-1):
        pt1 = end_point_list[i]
        pt2 = end_point_list[i+1]
        # pt_list = (lp.line_points(pt1,pt2,d))
        pt_list = (line_points(pt1,pt2,d))
        
        tot_pt_list.append(list(pt_list))
        if i != len(end_point_list)-2:
            tot_pt_list[i].pop(-1)
    flat_list = []
    for sublist in tot_pt_list:
        for element in sublist:
            element = list(element)
            # element = list(round(element,2))
            flat_list.append(element)
            # flat_list.append(round(element,2))
    return (flat_list)

# print(tot_point_list_generate(end_point_list,5))