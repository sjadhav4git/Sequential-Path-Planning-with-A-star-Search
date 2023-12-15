#!/bin/bash
# source /opt/ros/melodic/install/setup.bash
# /home/jetson/dofbot_ws/src/ub_dofbot_updated/src/joint_var_subscriber.py
# /home/jetson/dofbot_ws/src/ub_dofbot_updated/src/joint_var_publisher_launch.py



gnome-terminal -- bash -c  'source /opt/ros/melodic/install/setup.bash; python3 /home/jetson/dofbot_ws/src/ub_dofbot_updated/src/joint_var_subscriber.py; exec bash'
gnome-terminal -- bash -c  'source /opt/ros/melodic/install/setup.bash; python3 /home/jetson/dofbot_ws/src/ub_dofbot_updated/src/joint_var_publisher_launch.py; exec bash'
