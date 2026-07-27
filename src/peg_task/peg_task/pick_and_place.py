######### IMPORTS (directly copied from grasp_needle_active.py) #########

import copy
import numpy as np
import time
import sys
import os
import sys

import threading # temporary
from rclpy.executors import MultiThreadedExecutor

import rclpy
from rclpy.node import Node
from std_msgs.msg import Empty
from peg_interfaces.srv import GetObjectPose # sourcing ros workspaces will service file path apparent
from peg_control.psm1_cmd import Psm1Command
from peg_control.psm2_cmd import Psm2Command
from peg_control.tool_cmd import ToolCommand

from PyKDL import Vector, Rotation, Frame


# from scipy.spatial.transform import Rotation as R # Conversion between PyKDL Frame and numpy matrix
# from psm_arm import PSM # Patient Side Manipulator (PSM) interface
# from ecm_arm import ECM # Endoscopic Camera Manipulator (ECM) interface
# from kinematics.psmKinematics import PSMKinematicSolver # Kinematic solver for the PSM, which computes forward and inverse kinematics
# from simulation_manager import SimulationManager # Interface to the simulation manager, which manages the simulation environment and objects
# from utils.utilities import convert_mat_to_frame # Utility functions for converting between 4x4 numpy matrices and PyKDL Frames, and for performing Cartesian interpolation
# from utils.utilities import convert_frame_to_mat
# from utils.utilities import cartesian_interpolate_step # Utility function that, given a current frame and a target frame, computes the next incremental step towards the target frame
# from classes.tool_cmd import ToolCommand
from peg_math.conversions import ps_to_frame, rbs_to_frame
from peg_math.interpolation import cartesian_interpolate_step, cartesian_interpolate_step_new# Utility function that, given a current frame and a target frame, computes the next incremental step towards the target frame

# dynamic_path = os.path.abspath(__file__+"/../../")
# sys.path.append(dynamic_path)


#------------------------- OBJECT POSITION CLIENT NODE CLASS -------------------------#   
class ObjectPoseClient(Node):

    def __init__(self):
        super().__init__('object_pose_client') # Node name
        self.cli = self.create_client(GetObjectPose, '/get_object_pose')

        # while not self.cli.wait_for_service(timeout_sec=1.0):
        #     self.get_logger().info('service not available, waiting again...')

    def wait_for_server(self, timeout=10.0):
        if not self.cli.wait_for_service(timeout_sec=timeout):
            raise RuntimeError(
                f'/get_object_pose unavailable after {timeout}s — is object_loc running?'
            )

        
        self.req = GetObjectPose.Request()

    def get_object_pose(self, object_name:str):

        request = GetObjectPose.Request()
        request.object_name = object_name
        
        future = self.cli.call_async(request)
        #rclpy.spin_until_future_complete(self, future)
        while not future.done():
            time.sleep(0.01)

        return future.result()
    

#------------------------- AMBF SIM CONTROL  -------------------------#  

class SimControl(Node):

    def __init__(self):
        super().__init__('sim_controller') # Node name
        self.reset_bodies_cmd = self.create_publisher(Empty ,'/ambf/env/World/Command/Reset/Bodies', 1)
        self.reset_world_cmd = self.create_publisher(Empty, '/ambf/env/World/Command/Reset', 1)

    def reset_bodies(self): # Reset environment bodies
        self.reset_bodies_cmd.publish(Empty())

    def reset_env(self):
        self.reset_world_cmd.publish(Empty())

#------------------------- CLASS INSTANCES -------------------------#
rclpy.init()
object_pose_client = ObjectPoseClient() # Instance of service class
# psm1 = Psm1Command()
# psm2 = Psm2Command()

psm1 = ToolCommand('psm1')
psm2 = ToolCommand('psm2')

sim = SimControl()

#------------------------- HARD OFFSETS - check whether these apply to the block -------------------------#   

# Legacy Inits
psm1_init = [0.30780306382205863, -0.22222915389237488, 0.1423643360325034, -1.3613186165319513,0.5750600725456388, -0.8399263308008617] # Init joint position from the recording of old phantom
# psm2_init = [-0.46695894800579796, -0.17860657808832947, 0.15012366098379068,-1.0873261421084663, 0.7172512403887915, 0.48780102579228307]

#offset_psm1 = Frame(Rotation.RPY(-np.pi / 2., np.pi*1/3, 0.), # Fixed relative transform bewteen grasp body frame and the PSM tip frame, which defines how the needle is positioned relative to the robot's end-effector when grasped
#                    Vector(0.009973019361495972, -0.005215135216712952, 0.003237169608473778))

#offset_psm2 = Frame(Rotation.RPY(-np.pi / 2., 0., 0.),
#                     Vector(0.009973019361495972, -0.005215135216712952, 0.003237169608473778))

T_offset_w = Frame(Rotation.RPY(np.pi, 0.0, 0),
                             Vector(0.0, 0.0, 0.0))

# New Inits
psm2_init = [0.10, -0.30, 0.16, 0.0, 1.0, 0.5] # Custom init - good for grasping

psm2_grasp_offset = Frame(Rotation.RPY(0.0, 0.0, 0.0), Vector(-0.004, 0.01, 0.03)) # local offset to block
# maintain RPY from initialisation to keep 'claw grabber' like orientation

#psm1_grasp_offset = Frame(Rotation.RPY(np.pi / 8, np.pi, np.pi/4), Vector(0.0025, 0.001, 0.015)) # gripper RPY and position offset in z-direction - need to make it local to the block

#------------------------- PSM INIT -------------------------#
# # Check CRTK BASED CONTROL SCRIPT AND ALSO ORIGINAL PEG TRANSFER
def PsmInit(psm_arm: str):

    # Configure PSM joints to initilisation positions, set jaw angle
    if psm_arm == 'psm1':
        psm1.move_jp(psm1_init)
        psm1.set_jaw(0.25)
        psm_obj = psm1
        target_jp = psm1_init
    else:
        psm2.move_jp(psm2_init)
        psm2.set_jaw(0.25)
        psm_obj = psm2
        target_jp = psm2_init


    # Timer added to allow PSMs to reach initialised joint positions before measuring frames - prevents inaccurate early readings
    max_wait = 10.0
    start = time.time() # starts timer for elapsed time
    while time.time() - start < max_wait: # whilst under 10 seconds

        js = psm_obj.measured_js # measure curren joint state of psm

        # current_jp becomes measured joint state if measured js is not empty and has at least 1 value
        current_jp = js.position if js is not None and len(js.position) > 0 else None 

        # if updated current_jp has read valid data and this joint position is within 0.005 tolerance of target joint position, break loop and enable frame readings
        if current_jp is not None and np.allclose(current_jp, target_jp, atol=0.005):
            break
        time.sleep(0.002)
    else: # error detection
        print(f"WARNING: {psm_arm} did not converge to init position within {max_wait}s timeout")

    # Access target psm frames, transform
    if psm_arm == 'psm2':
        T_base_w = ps_to_frame(psm2.T_b_w) # Grab base in world pose from psm2/T_b_w and convert to frame
        T_ee_base = ps_to_frame(psm2.measured_cp) # Grab ee relative to base pose from psm2/measured_cp and convert to frame
        T_ee_w = T_base_w * T_ee_base # ee in world is multiplication of previous transforms
        # T_grip_base = T_ee_base * offset_psm2 # end-effector multiplied with offset of psm_tip

    else:
        T_base_w = ps_to_frame(psm1.T_b_w) # Grab base in world pose from psm1/T_b_w and convert to frame
        T_ee_base = ps_to_frame(psm1.measured_cp) # Grab ee relative to base pose from psm1/measured_cp and convert to frame
        T_ee_w = T_base_w * T_ee_base # ee in world is multiplication of previous transforms

        # Hardcoded offset between needle and PSM tip - how it moves relative to the PSM tip when grasped
    # Need to look into whether to use this as won't apply to the block as it is not a needle

    return T_base_w, T_ee_base, T_ee_w

#------------------------- CONTROL FUNCTIONS  -------------------------#

def psm_to_pose(psm, target_pose: Frame, success_flag: bool, control_speed=0.01, max_delta=0.01, pos_deadband=0.005, rot_deadband=0.01):
    success_flag = False

    while not success_flag:
        T_current = ps_to_frame(psm.measured_cp)
        #T_delta, success_flag = cartesian_interpolate_step(T_current, target_pose, max_delta=max_delta, deadband=pos_deadband)
        T_delta, success_flag = cartesian_interpolate_step_new(T_current, target_pose, max_delta, pos_deadband=pos_deadband,rot_deadband=rot_deadband)


        T_step = Frame() # New command frame that adds positional and rotational delta to current tool position
        T_step.p = T_current.p + T_delta.p # step positin = current position + delta position
        T_step.M = T_current.M * T_delta.M # step rotation = current rotation * delta rotation

        dist = (target_pose.p - T_current.p).Norm()
        rot = (T_current.M.Inverse() * target_pose.M).GetRPY()
        print(f"dist to target: {dist:.5f}, deadband: {pos_deadband}")
        print(T_delta.M)
        #print(T_step)

        psm.servo_cp(T_step) # Set cartesian pose of servo
        time.sleep(control_speed) # Adjustable speed so can slow down more intricate movements (e.g. pick and place)

#------------------------- RUN TASK LOOP -------------------------#  
def run_task():

#------------------------- RESET + INIT -------------------------#  
    sim.reset_env() # Reset all simulation bodies (e.g. blocks, PSMs)
    time.sleep(2.0)
    #T_base_w1, T_ee_base1, T_ee_w1 = PsmInit('psm1')
    T_base_w2, T_ee_base2, T_ee_w2 = PsmInit('psm2') # PSM initialisation
    time.sleep(3.0)

    #------------------------- OFFSET PROCESSING -------------------------#       
    # Get block position
    target_block = 'block5'
    block1 = object_pose_client.get_object_pose(target_block) # block1 in world frame
    T_block_w = rbs_to_frame(block1) # Convert block1 RigidBodyState to Frame

    # 'Claw-grabber' gripper orientation from init function - was a commanded jaw position, now translated into RPY
    R_desired_w = T_ee_w2.M # Target grasp orientation in world frame
    R_offset = (T_block_w.M).Inverse() * R_desired_w # Desired rotation offset converted to block frame

    # # ENTRANCE
    # position_offset = Vector(-0.004, 0.01, 0.06) # World frame position offset (6cm above the block)
    # p_entrance_w = T_block_w.p + position_offset # Add position offset to block in world

    # T_block_entrance = Frame(T_block_w.M * R_offset, p_entrance_w) # Apply R_offset relative to block's CURRENT rotation (composes, tracks the block) - this is still in the WORLD FRAME
    # T_cmd_entrance = T_base_w2.Inverse() * T_block_entrance # Convert block + offset in WORLD to block + offset in BASE for servo_cmd
     
    # # GRASP
    # position_offset = Vector(-0.002,0.001, 0.015)
    # p_grasp_w = T_block_w.p + position_offset

    # T_block_grasp = Frame(T_block_w.M * R_offset, p_grasp_w)
    # T_cmd_grasp = T_base_w2.Inverse() * T_block_grasp


    # # LIFT
    # T_block_ee = T_ee_w2.Inverse() * T_block_w # Grasp relationship between block and end-effector (block in end effector)

    # #position_offset = Vector(-0.004, 0.01, 0.06) # World frame position offset (6cm above the block)
    # position_offset = Vector(0,0,0.06)
    # p_lift_w = T_block_w.p + position_offset # blocks position in world + z-offset (lift block 6cm above blocks current position)

    
    # T_block_lift = Frame(T_block_w.M, p_lift_w) # lift block frame - target rotation and position, why am I using the blocks rotation?
    # T_desired_ee_w = T_block_lift * T_block_ee.Inverse() # Invert the grasp offset to solve for the ee pose that puts the block there in the world-frame
    # T_cmd_lift = T_base_w2.Inverse() * T_desired_ee_w # Convert from ee in world-frame to base-frame for servo_cp


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
    psm2.set_jaw(0.0)
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
    position_offset = Vector(0,0,0.06)
    p_lift_w = T_block_w.p + position_offset # blocks position in world + z-offset (lift block 6cm above blocks current position)

    
    T_block_lift = Frame(T_block_w.M, p_lift_w) # lift block frame - target rotation and position, why am I using the blocks rotation?
    T_desired_ee_w = T_block_lift * T_block_ee.Inverse() # Invert the grasp offset to solve for the ee pose that puts the block there in the world-frame
    T_cmd_lift = T_base_w2.Inverse() * T_desired_ee_w # Convert from ee in world-frame to base-frame for servo_cp

    Lift = False
    target_pose = T_cmd_lift
    max_delta = 0.003
    pos_deadband = 0.005
    rot_deadband = 0.01

    print(f"Lifting {target_block}")     
    while not Lift:
        T_current = ps_to_frame(psm2.measured_cp)

        T_delta, Lift = cartesian_interpolate_step_new(T_current, target_pose, max_delta, pos_deadband=pos_deadband,rot_deadband=rot_deadband)

        T_step = Frame() # New command frame that adds positional and rotational delta to current tool position
        T_step.p = T_current.p + T_delta.p # step positin = current position + delta position
        T_step.M = T_current.M * T_delta.M # step rotation = current rotation * delta rotation

        dist = (target_pose.p - T_current.p).Norm()
        rot = (T_current.M.Inverse() * target_pose.M).GetRPY()
        print(f"dist to target: {dist:.5f}, deadband: {pos_deadband}")
        print(f"rotational error {rot}, deadband: {rot_deadband}")
        print("Rot Diff ", rot)


        psm2.servo_cp(T_step) # Set cartesian pose of servo
        time.sleep(0.01) # Adjustable speed so can slow down more intricate movements (e.g. pick and place)

    print(f"Lifted{target_block}")
    time.sleep(2.0)
    # psm2.set_jaw(0.5)
    # time.sleep(2.0)

# Moved thread spinners to main function
# This is ros2 run command is looking at setup.py wrapper, which references 'main'
def main():
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
        run_task()
        
            
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
    