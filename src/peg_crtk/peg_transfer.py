 ######### IMPORTS (directly copied from grasp_needle_active.py) #########
# pyright: reportMissingImports=false

import copy
import numpy as np
import time
import sys
import os
import sys

import rclpy
from rclpy.node import Node
from peg_interfaces.srv import GetObjectPose # sourcing ros workspaces will service file path apparent

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
    
rclpy.init()
object_pose_client = ObjectPoseClient() # Instance of service class

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
        
    def command(self, frame: Frame): # takes in a frame, converts it to RigidBodyCmd format, publishes to '/ambf/env/psmx/baselink/Command'
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
#------------------------- SimManager CRTK Replacement  -------------------------#   


#------------------------- HELPER FUNCTIONS -------------------------#   
def pykdl_to_np(T_pykdl: Frame) -> np.matrix: # Converts a PyKDL Frame to a 4x4 numpy matrix
    rot_des = R.from_quat(T_pykdl.M.GetQuaternion()).as_matrix()
    pos_des = np.array([T_pykdl.p.x(), T_pykdl.p.y(), T_pykdl.p.z()])
    T_np = np.eye(4)
    T_np[0:3, 0:3] = rot_des
    T_np[0:3, 3] = pos_des
    return T_np

def np_to_pykdl(T_np: np.matrix) -> Frame: # Converts a 4x4 numpy matrix to a PyKDL Frame
    rot_des = np.squeeze(np.array(T_np[0:3, 0:3].reshape(-1, 1))).tolist()
    pos_des = np.squeeze(np.array(T_np[0:3, 3])).tolist()
    v = Vector(pos_des[0], pos_des[1], pos_des[2])
    r = Rotation(rot_des[0], rot_des[1], rot_des[2],
                 rot_des[3], rot_des[4], rot_des[5],
                 rot_des[6], rot_des[7], rot_des[8])
    T_pydkl = Frame(r, v)
    return T_pydkl

def gripper_to_yaw(T: Frame) -> Frame: # Converts a gripper frame to a yaw frame, taking into account the offset between the gripper and the yaw link of the robot
    L_yaw2ctrlpnt = 0.0
    offset_gripper = Frame(Rotation.RPY(0, 0, 0),
                           L_yaw2ctrlpnt * Vector(0.0, 0.0, -1.0))
    offset_x = Frame(Rotation.RPY(-np.pi/2, 0, 0), Vector(0.0, 0.0, 0.0))
    offset_y = Frame(Rotation.RPY(0, -np.pi/2, 0), Vector(0.0, 0.0, 0.0))
    T_out = T * offset_gripper * offset_x * offset_y
    return T_out

def yaw_to_gripper(T: Frame) -> Frame: # Converts a yaw frame to a gripper frame, taking into account the offset between the gripper and the yaw link of the robot
    L_yaw2ctrlpnt = 0.0
    offset_gripper = Frame(Rotation.RPY(0, 0, 0),
                           L_yaw2ctrlpnt * Vector(0.0, 0.0, 1.0))
    offset_x = Frame(Rotation.RPY(-np.pi/2, 0, 0), Vector(0.0, 0.0, 0.0))
    offset_y = Frame(Rotation.RPY(0, np.pi/2, 0), Vector(0.0, 0.0, 0.0))
    T_out =  T* offset_y * offset_x * offset_gripper
    return T_out

def set_jaw_angle(psm, jaw_angle = 0.0): # Quick function to set jaw angle without the need for if/else logi
    psm.set_jaw_angle(jaw_angle)

def psm_init(grasp_psm:str): # Need to clean-up
    
    if grasp_psm == 'psm1':
        psm1.move_jp(psm1_init)
        psm1.set_jaw_angle(0.3)
    else:
        psm2.move_jp(psm2_init)
        psm2.set_jaw_angle(0.3)
    
    time.sleep(3.0)

    if grasp_psm == 'psm2':
        T_psm_w_b = psm2.get_T_b_w()  # from world to PSM base
        T_psm_b_w = psm2.get_T_w_b()  # from PSM base to world
        # reads the current measured Cartesian pose and joint positions of PSM2, which are used to compute the forward kinematics to the tool tip and yaw link
        # appends a zero to the joint position array to account for missing elements
        psm2_pose_cp = psm2.measured_cp()
        psm2_pose = psm2.measured_jp()
        psm2_pose.append(0.0)
        # computes the forward kinematics for the tool tip and yaw link (link index 7 and 6 respectively) using the kinematic solver, which provides the transformation matrices for these links in the world frame
        mtx_tool_tip = psm_ks.compute_FK(psm2_pose, 7) ### FK to the tool tip
        mtx_tool_yaw = psm_ks.compute_FK(psm2_pose, 6) ### FK to the tool yaw link
        T_psm_yaw = convert_mat_to_frame(mtx_tool_yaw)
    else:
        T_psm_w_b = psm1.get_T_b_w()  # from world to PSM base
        T_psm_b_w = psm1.get_T_w_b()  # from PSM base to world
        psm1_pose_cp = psm1.measured_cp()
        psm1_pose = psm1.measured_jp()
        psm1_pose.append(0.0)
        mtx_tool_tip = psm_ks.compute_FK(psm1_pose, 7)  ### FK to the tool tip
        mtx_tool_yaw = psm_ks.compute_FK(psm1_pose, 6)  ### FK to the tool yaw link
        T_psm_yaw = convert_mat_to_frame(mtx_tool_yaw)

    # Hardcoded offset between needle and PSM tip - how it moves relative to the PSM tip when grasped
    # Need to look into whether to use this as won't apply to the block as it is not a needle
    if grasp_psm == 'psm2':
        T_eff_psmtip = offset_psm2
    else:
        T_eff_psmtip = offset_psm1

    return T_psm_w_b, T_psm_b_w, T_psm_yaw, T_eff_psmtip

def quat_to_rpy(q1,q2,q3,q4): # Custom quaternion to RPY function (equations in https://www.vcalc.com/wiki/quaternion-to-roll-pitch-yaw)
    roll = np.arctan2(2*((q4*q1)+(q2*q3)), (1-2*(np.power(q1,2)+np.power(q2,2))))
    pitch = np.arcsin(2*((q4*q2)-(q3*q1)))
    yaw = np.arctan2(2*((q4*q3)+(q1*q2)), (1-2*(np.power(q2,2)+np.power(q3,2))))

    return roll, pitch, yaw

def object_pose_format(object_name:str):
    obj_pose = object_pose_client.get_object_pose(object_name)
    object_position = Vector(obj_pose.pose.position.x, obj_pose.pose.position.y, obj_pose.pose.position.z)
    
    # convert orientation quaternion to RPY
    roll, pitch, yaw = quat_to_rpy(obj_pose.pose.orientation.x, obj_pose.pose.orientation.y, obj_pose.pose.orientation.z, obj_pose.pose.orientation.w)
    object_rotation = Rotation.RPY(roll, pitch,yaw)

    # Receives RigidBodyPose, Returns Frame
    return Frame(object_rotation, object_position)

def tool_command(frame, target_obj:str,  offset_pos, offset_rpy): # Calculate command to set end-effector pose to provided target location
    
    local_offset = Frame(Rotation.RPY(*offset_rpy), Vector(*offset_pos))  # Creates new frame with RPY offset and XYZ position offset
    working_frame = frames[frame]

    pose_frame = object_pose_format(target_obj) # retrieves current object pose and formats into suitable Frame(RPY Rot, Vector Pos)
     
    T_targetINw = pose_frame*local_offset # Target in world = position of target object (e.g. peg or block) with local offset applied
    T_toolINw_cmd = T_targetINw * working_frame.Inverse() # Command to set end-effector pose to target location

    return T_toolINw_cmd # Return for servo control

def servo_command(tool_pos, tool_command, psm, jaw_angle = 0.0, met_step = 0.001, rad_step = 0.005, speed=0.01): # Command sent to servo to set end-effector pose to provided target location
    Done = False

    while not Done: # Loop breaks when target position reached
        T_delta, Done = cartesian_interpolate_step(tool_pos, tool_command, met_step, rad_step) # Cartesian interpolation takes tunable steps, comparing current tool position with target position
        r_delta = T_delta.M.GetRPY() # Rotational delta (difference)

        T_cmd = Frame() # New command frame that adds positional and rotational delta to current tool position
        T_cmd.p = tool_pos.p + T_delta.p
        T_cmd.M = tool_pos.M * Rotation.RPY(r_delta[0], r_delta[1], r_delta[2])
        tool_pos = T_cmd
        T_move = yaw_to_gripper(T_psm_b_w * T_cmd * T_offset_w.Inverse()) # Translated to gripper movement through matrix multiplication through frames
        
        psm.servo_cp(T_move) # Set cartesian pose of servo
        #send_command('psm2', T_move)
        psm.set_jaw_angle(jaw_angle)
        time.sleep(speed) # Adjustable speed so can slow down more intricate movements (e.g. pick and place)

    return tool_pos # Return latest tool position to prevent teleportation

def send_command(object:str, frame: Frame, sleep_time=1.0):

    node = ObjectCommandPub(object)
    time.sleep(sleep_time)
    node.command(frame)
    time.sleep(sleep_time/2)
    print(f"Command send to {object}")
    node.destroy_node()
    
    
#------------------------- HARD OFFSETS -------------------------#   
psm1_init = [0.30780306382205863, -0.22222915389237488, 0.1423643360325034, -1.3613186165319513,0.5750600725456388, -0.8399263308008617] # Init joint position from the recording of old phantom
psm2_init = [-0.46695894800579796, -0.17860657808832947, 0.15012366098379068,-1.0873261421084663, 0.7172512403887915, 0.48780102579228307]

offset_psm1 = Frame(Rotation.RPY(-np.pi / 2., np.pi*1/3, 0.), # Fixed relative transform bewteen grasp body frame and the PSM tip frame, which defines how the needle is positioned relative to the robot's end-effector when grasped
                    Vector(0.009973019361495972, -0.005215135216712952, 0.003237169608473778))

offset_psm2 = Frame(Rotation.RPY(-np.pi / 2., 0., 0.),
                    Vector(0.009973019361495972, -0.005215135216712952, 0.003237169608473778))

T_offset_w = Frame(Rotation.RPY(np.pi, 0.0, 0),
                             Vector(0.0, 0.0, 0.0))

def main():
    #------------------------- GRAB -------------------------#   
    time.sleep(0.5)
    T_toolINw = copy.deepcopy(T_psmyaw_w)  # Give me the commanded position of the end effector to reach block1 given the following offsets
    T_toolINw_cmd = tool_command('effector', 'block1', (0.006, 0.001, 0.005), (0,0,0))
    print('Move to the desired pose')
    latest_pos = servo_command(tool_pos=T_toolINw, tool_command=T_toolINw_cmd, psm=psm2, jaw_angle=0.3)
    print("Position Reached")
    time.sleep(1.0)
    set_jaw_angle(psm2, 0.0) 
    time.sleep(2.0)
    # #------------------------- LIFT -------------------------#   
    # T_toolINw = copy.deepcopy(latest_pos) # Update current tool position
    # T_blockINw = object_pose_format('block1') # Find pose of block1 relative to tool-tip and add to 'frames' dictionary
    # T_block_psmtip = T_toolINw.Inverse()* T_blockINw
    # frames['grasp'] = T_block_psmtip
    # T_toolINw_cmd = tool_command('grasp', 'block1', (0.0, 0.0, 0.07), (0.3,0,0)) # 'GRASP' frame, 'block1' object, provide command pose for PSM to move block1 to block1 position with a z-offset of 0.07
    # print('Attempting to lift the block')
    # latest_pos = servo_command(T_toolINw, T_toolINw_cmd, psm2, 0.0, speed=0.03)
    # print("Lifted")
    # time.sleep(1.0)
    # #------------------------- RELOCATE -------------------------# 
    # T_toolINw = copy.deepcopy(latest_pos) # Update current tool position
    # T_blockINw = object_pose_format('block1') # Find pose of block1 relative to tool-tip and add to 'frames' dictionary
    # T_block_psmtip = T_toolINw.Inverse() * T_blockINw
    # frames['grasp'] = T_block_psmtip
    # T_toolINw_cmd = tool_command('grasp', 'peg10', (0.0, 0.0, 0.05), (0,0,0)) # 'GRASP' frame, 'peg10' object, provide command pose for PSM to move block1 to peg10 position with a yaw offset of 0.05
    # print('Attempting to relocate the block')
    # latest_pos = servo_command(T_toolINw, T_toolINw_cmd, psm2, 0.0)
    # print("Relocated")
    # time.sleep(2.0)
    # #------------------------- PLACE -------------------------#   
    # T_toolINw = copy.deepcopy(latest_pos)
    
    # # Recompute in case of any slip of the block - not entirely necessary
    # T_blockINw = object_pose_format('block1') # Find pose of block1 relative to tool-tip and add to 'frames' dictionary
    # T_block_psmtip = T_toolINw.Inverse() * T_blockINw
    # frames['grasp'] = T_block_psmtip

    # # Added 45 degree yaw to prevent arm getting in the way when placing
    # T_toolINw_cmd = tool_command('grasp', 'peg10', (0.0, 0.0, 0.004), (0,0,np.pi/4))
    # print('Attempting to place the block')
    # latest_pos = servo_command(T_toolINw, T_toolINw_cmd, psm2, 0.0, speed=0.02)
    # print("Placed")
    # time.sleep(2.0)

if __name__ == '__main__':
    simulation_manager = SimulationManager('grasp_block') # Connects to the simulation under the client name 'grasp_block'
    time.sleep(0.2)
    w = simulation_manager.get_world_handle() # Get the world handle from the simulation manager, which allows for resetting and managing all objects in the simulation
    time.sleep(0.2)
    w.reset_bodies()
    time.sleep(0.2)

    tool_id = 420006 # the tool id for the real psm
    psm_ks = PSMKinematicSolver(psm_type=tool_id, tool_id=tool_id) # Kinematic solver for the PSM (specific tool ID), which computes forward and inverse kinematics
    
    ############################################## SWAP TO ROS
    cam = ECM(simulation_manager, "CameraFrame") # Commands ECM via servo_jp to a specific joint configuration, which positions the camera in a desired pose for the task
    cam.servo_jp([0.0, 0.05, -0.01, 0.0])
    time.sleep(0.2)
    ############################################## SWAP TO ROS
    psm1 = PSM(simulation_manager, "psm1", add_joint_errors=False, tool_id=tool_id)
    time.sleep(0.2)
    ############################################## SWAP TO ROS
    psm2 = PSM(simulation_manager, "psm2", add_joint_errors=False, tool_id=tool_id)
    time.sleep(0.2)
    
    grasp_arm = 'psm2' # Hard-coded grasping arm - change this to be applied in function
    T_psm_w_b, T_psm_b_w, T_psm_yaw, T_eff_psmtip = psm_init(grasp_arm) # Initialise PSM offsets

    T_psmyaw_w = T_psm_w_b * T_psm_yaw * T_offset_w ## == TtoolInworld

    frames = {
    'effector': T_eff_psmtip, #transform between end-effector and PSM (actually the hard-coded needle offset)
    }
    
    try:
        main()
    finally:
        object_pose_client.destroy_node()
        rclpy.shutdown()




