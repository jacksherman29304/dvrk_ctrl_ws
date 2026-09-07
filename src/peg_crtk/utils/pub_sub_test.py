 ######### IMPORTS (directly copied from grasp_needle_active.py) #########
# pyright: reportMissingImports=false

import numpy as np
import time
import sys
import os
import sys
import time

import rclpy
from rclpy.node import Node
from peg_transfer_interfaces.srv import GetObjectPose # sourcing ros workspaces will service file path apparent

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
from ambf_msgs.msg import RigidBodyState, RigidBodyCmd

dynamic_path = os.path.abspath(__file__+"/../../")
sys.path.append(dynamic_path)


#------------------------- OBJECT COMMAND PUBLISHER -------------------------#   
class ObjectCommandPub(Node):
    def __init__(self, psm: str):
        super().__init__('object_command_publisher') # Node name
        namespace = "/py/"
        self.psm = psm

        self.psm_cmd_pub = self.create_publisher(
            RigidBodyCmd, # publisher to custom topic name with RigidBodyCmd message type (Pose command)
            namespace + self.psm + "/command_pose", 
             10)
        
    def command(self, frame: Frame):
        msg = RigidBodyCmd()

        pos = frame.p # extract frame position

        rot = frame.M # extract frame rotation
        qx, qy, qz, qw = rot.GetQuaternion()

        # Update position
        msg.pose.position.x = pos.x()
        msg.pose.position.y = pos.y()
        msg.pose.position.z = pos.z()

        # Update orientation
        msg.pose.orientation.x = float(qx)
        msg.pose.orientation.y = float(qy)
        msg.pose.orientation.z = float(qz)
        msg.pose.orientation.w = float(qw)
        
        self.psm_cmd_pub.publish(msg) # publish Pose to topic


def send_command(object:str, frame: Frame, sleep_time=1.0):

    node = ObjectCommandPub(object)
    time.sleep(sleep_time)
    node.command(frame)
    time.sleep(sleep_time/2)
    print(f"Command send to {object}")
    node.destroy_node()
    


Transform = Frame(Rotation.RPY(10, 0, 0), Vector(10, 0.0, 0.0))  # nonzero offset for a visible test


rclpy.init()
send_command('psm2', Transform)
rclpy.shutdown()

# psm2 = ObjectCommandPub('psm2') # setup psm2 command line

# time.sleep(1.0)              # let discovery complete
# psm2.command(T)           # send command to psm2
# time.sleep(0.5)               # let the message actually flush before shutdown
# psm2.destroy_node()
# rclpy.shutdown()

