 ######### IMPORTS (directly copied from grasp_needle_active.py) #########
# pyright: reportMissingImports=false

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
from utility_interfaces.srv import GetObjectPose # sourcing ros workspaces will service file path apparent

from PyKDL import Vector, Rotation, Frame
from scipy.spatial.transform import Rotation as R # Conversion between PyKDL Frame and numpy matrix
from psm_arm import PSM # Patient Side Manipulator (PSM) interface
from ecm_arm import ECM # Endoscopic Camera Manipulator (ECM) interface
from kinematics.psmKinematics import PSMKinematicSolver # Kinematic solver for the PSM, which computes forward and inverse kinematics
from simulation_manager import SimulationManager # Interface to the simulation manager, which manages the simulation environment and objects

from utils.utilities import convert_mat_to_frame # Utility functions for converting between 4x4 numpy matrices and PyKDL Frames, and for performing Cartesian interpolation
from utils.utilities import convert_frame_to_mat
from utils.utilities import cartesian_interpolate_step # Utility function that, given a current frame and a target frame, computes the next incremental step towards the target frame

from geometry_msgs.msg import Pose
from ambf_msgs.msg import RigidBodyCmd

from classes.tool_cmd import ToolCommand
from helpers import ps_to_frame

dynamic_path = os.path.abspath(__file__+"/../../")
sys.path.append(dynamic_path)


#------------------------- OBJECT POSITION CLIENT NODE CLASS -------------------------#   
class ObjectPoseClient(Node):

    def __init__(self):
        super().__init__('object_pose_client') # Node name
        self.cli = self.create_client(GetObjectPose, '/get_object_pose')

        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        
        self.req = GetObjectPose.Request()

    def get_object_pose(self, object_name:str):

        request = GetObjectPose.Request()
        request.object_name = object_name
        
        future = self.cli.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        return future.result()
    

# #------------------------- PSM INIT -------------------------# 
# def psm_init(psm: str):
    
#     if psm == 'psm1':
#         psm1_cmd.servo_jp(psm1_init)
#         psm1_cmd.set_jaw(0.3)
#     else:
#         psm2_cmd.servo_jp(psm2_init)
#         psm2_cmd.set_jaw(0.3)

#     time.sleep(2.0)

#     if psm == 'psm2':
#         T_psm_w_b = ps_to_frame(psm2_cmd.T_b_w) # world to PSM base
#         T_psm_b_w = T_psm_w_b.Inverse() # PSM base to world
#         psm2_pose_cp = psm2_cmd.measured_cp
#         psm2_pose = list(psm2_cmd.measured_js.position)
#         psm2_pose.append(0.0)
#         #### EVENTUALLY REPLACE FK
#         mtx_tool_tip = psm_ks.compute_FK(psm2_pose, 7) ### FK to the tool tip
#         mtx_tool_yaw = psm_ks.compute_FK(psm2_pose, 6) ### FK to the tool yaw link
#         T_psm_yaw = convert_mat_to_frame(mtx_tool_yaw)

#     else:
#         T_psm_w_b = ps_to_frame(psm1_cmd.T_b_w) # world to PSM base
#         T_psm_b_w = T_psm_w_b.Inverse() # PSM base to world
#         psm1_pose_cp = psm1_cmd.measured_cp
#         psm1_pose = list(psm1_cmd.measured_js.position)
#         psm1_pose.append(0.0)

#         mtx_tool_tip = psm_ks.compute_FK(psm1_pose, 7)  ### FK to the tool tip
#         mtx_tool_yaw = psm_ks.compute_FK(psm1_pose, 6)  ### FK to the tool yaw link
#         T_psm_yaw = convert_mat_to_frame(mtx_tool_yaw)

#     if psm == 'psm2':
#         T_eff_psmtip = offset_psm2
#     else:
#         T_eff_psmtip = offset_psm1

#     return T_psm_w_b, T_psm_b_w, T_psm_yaw, T_eff_psmtip

       
       
# #------------------------- HARD OFFSETS -------------------------#   
# psm1_init = [0.30780306382205863, -0.22222915389237488, 0.1423643360325034, -1.3613186165319513,0.5750600725456388, -0.8399263308008617] # Init joint position from the recording of old phantom
# psm2_init = [-0.46695894800579796, -0.17860657808832947, 0.15012366098379068,-1.0873261421084663, 0.7172512403887915, 0.48780102579228307]

# offset_psm1 = Frame(Rotation.RPY(-np.pi / 2., np.pi*1/3, 0.), # Fixed relative transform bewteen grasp body frame and the PSM tip frame, which defines how the needle is positioned relative to the robot's end-effector when grasped
#                     Vector(0.009973019361495972, -0.005215135216712952, 0.003237169608473778))

# offset_psm2 = Frame(Rotation.RPY(-np.pi / 2., 0., 0.),
#                     Vector(0.009973019361495972, -0.005215135216712952, 0.003237169608473778))

# T_offset_w = Frame(Rotation.RPY(np.pi, 0.0, 0),
#                              Vector(0.0, 0.0, 0.0))

def main():
    time.sleep(0.5)
    T = Frame(Rotation.RPY(0,0,0), Vector(10,0,0))
    psm1_cmd.servo_cp(T)
    time.sleep(0.5)
    # need to make psm innit first




rclpy.init()
object_pose_client = ObjectPoseClient() # Instance of service class

if __name__ == '__main__':

    # psm1 and psm2 command objects of the ToolCommand class
    psm1_cmd = ToolCommand('psm1')
    time.sleep(0.2)
    psm2_cmd = ToolCommand('psm2')
    time.sleep(0.2)

    executor = MultiThreadedExecutor()
    executor.add_node(psm1_cmd)
    executor.add_node(psm2_cmd)
    executor.add_node(object_pose_client)

    spin_thread = threading.Thread(target=executor.spin, daemon=True)
    spin_thread.start()

    # rclpy.spin(psm1_cmd)
    # rclpy.spin(psm2_cmd)



    # T_psm_w_b, T_psm_b_w, T_psm_yaw, T_eff_psmtip = psm_init('psm2') # Initialise PSM offsets
    # T_psmyaw_w = T_psm_w_b * T_psm_yaw * T_offset_w ## UNDERSTAND THIS ###############

    # frames = {
    # 'effector': T_eff_psmtip, #transform between end-effector and PSM (actually the hard-coded needle offset)
    # }

    try:
        main()
    finally:
        psm1_cmd.destroy_node()
        psm2_cmd.destroy_node()
        object_pose_client.destroy_node()
        rclpy.shutdown()


#psm1_command = ObjectCommandPub('psm1')
#psm1_command.command(Pose) # my node not working - fiddle with eventually
#pose = object_pose_client.get_object_pose('psm1')