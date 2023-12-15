#! /usr/bin/env python

import rospy
import puzzle_solver.final_main_method_random_samples_1 as solve
import dofbot_controller_original_copy.detailed_final_path_generator as dfpg
# import utils.detailed_path_viewer as dpv
import my_inverse_kinematics.main_inv_kin as IK
import sys
import capture_image.capture_puzzle_optimized as CAP_img

SOLVE = solve.solver()
PG = dfpg.Path_Generate()
# DPV = dpv.Movements()

def capture_solve_save(iterations,visualize):
    rospy.loginfo("Capturing_puzzle")
    CAP_img.main_capture()
    rospy.loginfo("Solving_puzzle ")
    SOLVE.solve_final_optimized(iterations)
    if visualize: 
        rospy.loginfo("Visualizing...")
        SOLVE.visualize(200,False) # this visualizes a puzzle movements.
    rospy.loginfo("Generating path")
    PG.detailed_path_generate(0,30,5)
    rospy.loginfo("solvig inverse kinematics")
    IK.main_ik()
    rospy.loginfo("All data collected, created and saved\n")
    # DPV.detailed_viewer(100) # This line visualizeses all movements in 3d