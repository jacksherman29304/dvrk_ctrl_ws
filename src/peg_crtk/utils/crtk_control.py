######### IMPORTS #########

#Imports ROS messages for timestamped 3D pose (position and orientation) - cartesian
#Type: geometry_msgs/
from geometry_msgs.msg import PoseStamped
#Imports ROS messages for joint state (position (rad or m), velocity (rad/s or m/s), effort (Nm or N)) - joint
#Type: sensor_msgs/msg/
from sensor_msgs.msg import JointState
#Imports ROS messagse for timestamped twist with reference coordinate frame
from geometry_msgs.msg import TwistStamped
#Imports RAL (ROS Abstraction Layer) for ROS1 and ROS2 compatibility (node creation, publisher/subscriber creation, etc.)
from ros_abstraction_layer import ral
import math
#Rotation class used to represent and convert 3D rotation in various formats (e.g., rotation matrix, quaternion, Euler angles)
from PyKDL import Vector, Rotation, Frame
#Import all from unit-conversion helpers - specifically SimToSI.linear_factor is used to convert from simulation units to SI units (meters)
from units_conversion import *

import rclpy
from rclpy.node import Node
from peg_transfer_interfaces.srv import GetObjectPose # sourcing ros workspaces will service file path apparent


# psm2 = PSM(simulation_manager, "psm2", add_joint_errors=False, tool_id=tool_id)

class CrtkControl(Node):

    def __init__(self, psm:str):
        namespace = "/CRTK/"
        self.psm = psm
        self.measured_js_topic = namespace + self.psm + "/measured_js"
        self.measured_cp_topic = namespace + self.psm + "/measured_cp"
        self.servo_jp_topic = namespace + self.psm + "/servo_jp"
        self.servo_cp_topic = namespace + self.psm + "/servo_cp"

        self.measured_js = JointState()
        self.measured_cp = PoseStamped()

        self.servo_jp_msg = JointState()
        self.servo_cp_msg = PoseStamped()

        # Initial 6-DOF Joint array for the robot (outer yaw, outer pitch, insertion/prismatic, outer roll, wrist pitch, wrist yaw)
        self.servo_jp_msg.position = [0., 0., 0.1 * SimToSI.linear_factor, 0., 0., 0.]

        # Set initial position of the robot's end-effector in Cartesian space (x, y, z) in meters (converted from simulation units)
        self.servo_cp_msg.pose.position.x = 0.0 * SimToSI.linear_factor # 0
        self.servo_cp_msg.pose.position.y = 0.0 * SimToSI.linear_factor # 0
        self.servo_cp_msg.pose.position.z = -0.1 * SimToSI.linear_factor # -0.1 below ref point
        # Rotation matrix: roll = 3.14 rad (180 deg), pitch = 0 rad, yaw = 1.57079 rad (90 deg)
        R_7_0 = Rotation.RPY(3.14, 0.0, 1.57079)
        # R_P_7_0 converted in quaternion format (x, y, z, w)
        # Assigns each component to pose message's orientation field (x, y, z, w)
        self.servo_cp_msg.pose.orientation.x = R_7_0.GetQuaternion()[0]
        self.servo_cp_msg.pose.orientation.y = R_7_0.GetQuaternion()[1]
        self.servo_cp_msg.pose.orientation.z = R_7_0.GetQuaternion()[2]
        self.servo_cp_msg.pose.orientation.w = R_7_0.GetQuaternion()[3]

        # subscribers
        self.measured_js_sub = self.create_subscriber(self.measured_js_topic, JointState, self.measured_js_cb, 1)
        self.measured_cp_sub = self.create_subscriber(self.measured_cp_topic, PoseStamped, self.measured_cp_cb, 1)

        # publishers
        self.servo_jp_pub = self.create_publisher(self.servo_jp_topic, JointState, 1)
        self.servo_cp_pub  = self.create_publisher(self.servo_cp_topic, PoseStamped, 1)


    def measured_js_cb(self, msg):
        self.measured_js = msg

    def measured_cp_cb(self, msg):
        self.measured_cp = msg

    def servo_cp(self, frame: Frame):
        msg = PoseStamped()

        pos = frame.p # extract frame position vector
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
        
        self.servo_cp_pub.publish(msg) # publish Pose to cp topic

    def servo_jp(self, joint_positions: list):
        msg = JointState()

        msg.position = list(joint_positions)

        self.servo_jp_pub.publish(msg)
    


crtk = CrtkControl()




        

