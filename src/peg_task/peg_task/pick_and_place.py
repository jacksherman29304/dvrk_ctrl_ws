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

# Control Imports
from peg_control.tool_cmd import ToolCommand

# Task imports
from peg_task.config import load_config
from peg_task.ros_interface import ObjectPoseClient, SimControl
from peg_task.routines import PsmInit
from peg_task.motion import psm_to_pose


#------------------------- CLASS INSTANCES -------------------------#
rclpy.init()
object_pose_client = ObjectPoseClient() # Instance of service class
psm1 = ToolCommand('psm1')
psm2 = ToolCommand('psm2')
sim = SimControl()

#------------------------- RUN TASK LOOP -------------------------#  
def run_task(parameters):
#------------------------- RESET + INIT -------------------------#  
    params = parameters
    sim.reset_env() # Reset all simulation bodies (e.g. blocks, PSMs)
    time.sleep(2.0)
    #T_base_w1, T_ee_base1, T_ee_w1 = PsmInit('psm1')
    #T_base_w2, T_ee_base2, T_ee_w2 = PsmInit('psm2') # PSM initialisation
    T_base_w2, T_ee_base2, T_ee_w2 = PsmInit(psm=psm2, jp_init=params['init']['psm2_init'], jaw_init=params['init']['jaw_open'], max_wait=10)
    time.sleep(3.0)

    #------------------------- OFFSET PROCESSING -------------------------#       
    # Get block position
    target_block = 'block5'
    block1 = object_pose_client.get_object_pose(target_block) # block1 in world frame
    T_block_w = rbs_to_frame(block1) # Convert block1 RigidBodyState to Frame

    # 'Claw-grabber' gripper orientation from init function - was a commanded jaw position, now translated into RPY
    R_desired_w = T_ee_w2.M # Target grasp orientation in world frame
    R_offset = (T_block_w.M).Inverse() * R_desired_w # Desired rotation offset converted to block frame

#------------------------- ENTRANCE OPERATION -------------------------#   
    # ENTRANCE
    position_offset = Vector(-0.004, 0.01, 0.06) # World frame position offset (6cm above the block)
    p_entrance_w = T_block_w.p + position_offset # Add position offset to block in world

    T_block_entrance = Frame(T_block_w.M * R_offset, p_entrance_w) # Apply R_offset relative to block's CURRENT rotation (composes, tracks the block) - this is still in the WORLD FRAME
    T_cmd_entrance = T_base_w2.Inverse() * T_block_entrance # Convert block + offset in WORLD to block + offset in BASE for servo_cmd
     
    Enter = False # Interpolation success flag
    print(f"Entering scene for {target_block}")
    psm_to_pose(psm=psm2, target_pose=T_cmd_entrance, success_flag=Enter, max_delta=0.01, pos_deadband=0.005)
    time.sleep(2.0)

#------------------------- GRAB OPERATION -------------------------#
    # GRASP
    position_offset = Vector(-0.002,0.001, 0.015)
    p_grasp_w = T_block_w.p + position_offset

    T_block_grasp = Frame(T_block_w.M * R_offset, p_grasp_w)
    T_cmd_grasp = T_base_w2.Inverse() * T_block_grasp

    Grasp = False # Interpolation success flag
    print(f"Moving to {target_block}")
    psm_to_pose(psm=psm2, target_pose=T_cmd_grasp, success_flag=Grasp, max_delta=0.003, pos_deadband=0.005) # Need to make sure error allowance is within the size of the block
    print(f"Arrived at {target_block}")

    # Close Jaws
    time.sleep(2.0)
    psm2.set_jaw(0.05) # can't be completely zero
    time.sleep(2.0)

# #------------------------- LIFT OPERATION -------------------------#  
    # LIFT

    # Needed to update T_ee_w2 and block position in wold so just hard-coded it here 
    # In future, edit psm_init function to have a boolean that either recalcs these variables or recalcs and commands to init pos
    # Need to carry over the object format function here as well
    T_base_w = ps_to_frame(psm2.T_b_w) # Grab base in world pose from psm2/T_b_w and convert to frame
    T_ee_base = ps_to_frame(psm2.measured_cp) # Grab ee relative to base pose from psm2/measured_cp and convert to frame
    T_ee_w2 = T_base_w * T_ee_base # ee in world is multiplication of previous transforms

    target_block = 'block5'
    block1 = object_pose_client.get_object_pose(target_block) # block1 in world frame
    T_block_w = rbs_to_frame(block1) # Convert block1 RigidBodyState to Frame
    # -------------------------- FIX ABOVE (and below) -------------------------
    
    T_block_ee = T_ee_w2.Inverse() * T_block_w # Grasp relationship between block and end-effector (block in end effector)

    #position_offset = Vector(-0.004, 0.01, 0.06) # World frame position offset (6cm above the block)
    position_offset = Vector(0,0,0.05)
    p_lift_w = T_block_w.p + position_offset # blocks position in world + z-offset (lift block 6cm above blocks current position)

    T_block_lift = Frame(T_block_w.M, p_lift_w) # lift block frame - target rotation and position, why am I using the blocks rotation?
    T_desired_ee_w = T_block_lift * T_block_ee.Inverse() # Invert the grasp offset to solve for the ee pose that puts the block there in the world-frame
    T_cmd_lift = T_base_w2.Inverse() * T_desired_ee_w # Convert from ee in world-frame to base-frame for servo_cp

    Lift = False
    print(f"Lifting {target_block}")    
    psm_to_pose(psm=psm2, target_pose=T_cmd_lift, success_flag=Lift, max_delta=0.003, pos_deadband=0.005, rot_deadband=0.01)
    print(f"Lifted{target_block}")
    time.sleep(2.0)

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
    