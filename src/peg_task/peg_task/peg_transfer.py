# RCLPY Imports
import rclpy
import threading
from rclpy.executors import MultiThreadedExecutor

# External Imports
from PyKDL import Vector, Rotation, Frame
import numpy as np
import time

# Math Imports
from peg_math.conversions import ps_to_frame, rbs_to_frame
from peg_math.interpolation import cartesian_interpolate_step, cartesian_interpolate_step_new # Utility function that, given a current frame and a target frame, computes the next incremental step towards the target frame
from peg_math.plotters import plot_error

# Control Imports
from peg_control.tool_cmd import ToolCommand

# Task imports
from peg_task.config import load_config
from peg_task.ros_interface import ObjectPoseClient, SimControl
from peg_task.routines import PsmInit, get_object_pose, init_handlers
from peg_task.routines import enter_scene, grasp_block, lift_block, relocate_block, place_block
from peg_task.motion import psm_to_pose


#------------------------- CLASS INSTANCES -------------------------#
rclpy.init()
object_pose_client = ObjectPoseClient() # Instance of service class
psm1 = ToolCommand('psm1')
psm2 = ToolCommand('psm2')
sim = SimControl()

init_handlers(object_pose_client) # pass client-side handler to routines,py

#------------------------- RUN TASK LOOP -------------------------#  
def run_task(parameters):

    params = parameters # parameters.yaml - offsets, objects etc.
    sim.reset_env() # Reset all simulation bodies (e.g. blocks, PSMs)
    time.sleep(2.0)
    T_base_w2, T_ee_base2, T_ee_w2 = PsmInit(psm=psm2, jp_init=params['init']['psm2_init'], jaw_init=params['init']['jaw_open'], max_wait=10)
    time.sleep(3.0)

    target_arm = psm2
    #------------------------- GET BLOCK  -------------------------#   
    T_block_w = get_object_pose(params['target_block'])

    # 'Claw-grabber' gripper orientation from init function - was a commanded jaw position, now translated into RPY
    R_desired_w = T_ee_w2.M # Target grasp orientation in world frame
    R_offset = (T_block_w.M).Inverse() * R_desired_w # Desired rotation offset converted to block frame

#------------------------- ENTRANCE OPERATION -------------------------#   
    enter_scene(target_arm)
#------------------------- GRASP OPERATION -------------------------#
    grasp_block(target_arm)
# #------------------------- LIFT OPERATION -------------------------#  
    lift_block(target_arm)
# #------------------------- RELOCATE OPERATION -------------------------#  
    relocate_block(target_arm)
# #------------------------- PLACE OPERATION -------------------------#  
    place_block(target_arm)

# Moved thread spinners to main function
# This is ros2 run command is looking at setup.py wrapper, which references 'main'
def main():
    parameters = load_config()
    executor = MultiThreadedExecutor()
    executor.add_node(psm1)
    executor.add_node(psm2)
    executor.add_node(object_pose_client)
    executor.add_node(sim)
    
    spin_thread = threading.Thread(target=executor.spin, daemon=True)
    spin_thread.start()
    
        # T_psm_w_b, T_psm_b_w, T_psm_yaw, T_eff_psmtip = psm_init('psm2') # Initialise PSM offsets
        # T_psmyaw_w = T_psm_w_b * T_psm_yaw * T_offset_w ## UNDERSTAND THIS ###############
    
        # frames = {
        # 'effector': T_eff_psmtip, #transform between end-effector and PSM (actually the hard-coded needle offset)
        # }
    
    try:
        object_pose_client.wait_for_server()
        sim.reset_env()
        run_task(parameters)
        
            
    finally:
        executor.shutdown()
        spin_thread.join(timeout=2.0)
        psm1.destroy_node()
        psm2.destroy_node()
        object_pose_client.destroy_node()
        sim.destroy_node()
        rclpy.shutdown()

# anything in here is invisivle to ros2 run
if __name__ == '__main__':
    main()
    