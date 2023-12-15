#! /usr/bin/env python

x_cords = [Int for Int in range(-65,61,30)]
# y_cords = [Int for Int in range(270,149,-30)]
y_cords = [Int for Int in range(240,119,-30)]

# adding extra lengths:
touch_list = []
safe_height_list = []

def p_list(z):
    all_locations = []
    for y in y_cords:
        for x in x_cords:
            all_locations.append([x,y,z])
    return all_locations

def center_finder(pt1,pt2):
    # pt1 = [x,y,z]
    # pt2 = [x,y,z]
    if(pt1[1]==pt2[1]):
        x_new = (pt1[0]+pt2[0])/2
        y_new = pt1[1]
    if(pt1[0]==pt2[0]):
        y_new = (pt1[1]+pt2[1])/2
        x_new = pt1[0]
    z_new = pt1[2]+10
    return [x_new,y_new,z_new]

def pt_list(path_list,touch_z,safe_z):

    touch_list = p_list(touch_z)
    safe_height_list = p_list(safe_z)

    # path_list = [[2,1],[6,2],[10,6],[11,10],[7,11],[6,7],[5,6]]

    final_path_pt_list = []
    for path in path_list:
        final_path_pt_list.append(safe_height_list[path[0]-1])
        final_path_pt_list.append(touch_list[path[0]-1])
        final_path_pt_list.append(touch_list[path[1]-1])
        final_path_pt_list.append(safe_height_list[path[1]-1])
        ##############################
        
    return final_path_pt_list