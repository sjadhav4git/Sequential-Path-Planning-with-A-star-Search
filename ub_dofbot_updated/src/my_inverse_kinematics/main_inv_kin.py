import json
import utils.inv_kin_functions as IK
import sys
from tqdm import tqdm

def main_ik():
    
    
    """
    Run this function to save all joint variables to joint_var.json file in database
    """
    print("\nSolving inverse kinematics\nwait...")
    with open("src/database/dofbot_details.json","r") as json_read:
        data = json.load(json_read)

    l1,l2,l3,l4,finger_len,circum_points = data['l1'],data['l2'],data['l3'],data['l4'],data['finger_len'],data['circum_points']

    l4 += finger_len
    with open("src/database/detailed_final_path.json","r") as json_read:
        data = json.load(json_read)

    final_path_co_ords = data["final_path"]
    # total = len(final_path_co_ords)
    i = 1
    joint_var_angles = []
    joint_var_locations = []
    # print("count:\n")
    total_itr = len(final_path_co_ords)
    progress_bar = tqdm(total=total_itr, desc="Solving Inverse Kinematics: ")
    
    for pt in final_path_co_ords:
        # print(i,'/',total,end="")
        # sys.stdout.flush()
        th_1,th_2,th_3,th_4,J1_pt,J2_pt,J3_pt,J4_pt = IK.joint_variables(pt,l1,l2,l3,l4,circum_points)
        joint_var_angles.append((th_1,th_2,th_3,th_4))
        joint_var_locations.append((J1_pt,J2_pt,J3_pt,J4_pt))
        progress_bar.update(1)
        # print("\r")
    progress_bar.close()
    data = {
        "joint_var_angles" : joint_var_angles,
        "joint_var_locations" : joint_var_locations
    }

    with open("src/database/joint_var.json","w") as json_write:
        json.dump(data,json_write,indent=4)


    # print(l1,l2,l3,l4,finger_len,circum_points)
    # P = [100,100,100]
    # print(IK.joint_variables(P,l1,l2,l3,l4,circum_points))
    # print(len(final_path_co_ords))
    
    
    
    
    
    
    #---------------------------------------------------------------
    # Return_fun:
def main_ik_return():
    """
    Run this function to save all joint variables to joint_var.json file in database
    """
    print("\nSolving inverse kinematics\nwait...")
    with open("src/database/dofbot_details.json","r") as json_read:
        data = json.load(json_read)

    l1,l2,l3,l4,finger_len,circum_points = data['l1'],data['l2'],data['l3'],data['l4'],data['finger_len'],data['circum_points']

    l4 += finger_len
    with open("src/database/detailed_final_path.json","r") as json_read:
        data = json.load(json_read)

    final_path_co_ords = data["final_path"]
    # total = len(final_path_co_ords)
    i = 1
    joint_var_angles = []
    joint_var_locations = []
    # print("count:\n")
    total_itr = len(final_path_co_ords)
    progress_bar = tqdm(total=total_itr, desc="Solving Inverse Kinematics: ")
    
    for pt in final_path_co_ords:
        # print(i,'/',total,end="")
        # sys.stdout.flush()
        th_1,th_2,th_3,th_4,J1_pt,J2_pt,J3_pt,J4_pt = IK.joint_variables(pt,l1,l2,l3,l4,circum_points)
        joint_var_angles.append((th_1,th_2,th_3,th_4))
        joint_var_locations.append((J1_pt,J2_pt,J3_pt,J4_pt))
        progress_bar.update(1)
        # print("\r")
    progress_bar.close()
    data = {
        "joint_var_angles" : joint_var_angles,
        "joint_var_locations" : joint_var_locations
    }

    with open("src/database/joint_var.json","w") as json_write:
        json.dump(data,json_write,indent=4)


    # print(l1,l2,l3,l4,finger_len,circum_points)
    # P = [100,100,100]
    # print(IK.joint_variables(P,l1,l2,l3,l4,circum_points))
    # print(len(final_path_co_ords))