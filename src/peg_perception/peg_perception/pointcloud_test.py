# Math & transformation imports
import numpy as np
import open3d as o3d
import matplotlib.colors as cls
import copy
import PyKDL
import time

# RCLPY Imports
import rclpy
import threading
from rclpy.executors import MultiThreadedExecutor

# Peg Task and Control imports for PSM demonstration
from peg_control.tool_cmd import ToolCommand
from peg_task.config import load_config
from peg_task.ros_interface import ObjectPoseClient, SimControl
from peg_task.routines import PsmInit, init_handlers
from peg_task.routines import get_object_pose, enter_scene, move_gripper_to_pose
from peg_task.motion import psm_to_pose
from peg_math.conversions import ps_to_frame


# ----------------------------------- PEGBOARD 
# ---- POINTCLOUD COLOUR MASKING

# left stereo camera depth data from ROS topic /ambf/env/stereo/left/DepthData (generated in camera_interface.py)
data = np.load('/home/dvrk-team/Desktop/pointcloudL_curr.npy') 

# point data in columns 0-2 (x,y,z)
points = data[:, 0:3] 

# rgb data in column 3
rgb = data[:,3] # column 3 (rgb)

# reinterpret float32 bits as uint32
rgb_uint = rgb.view(np.uint32)

# extract rgb (rrrrrrrr gggggggg bbbbbbbb)
r = (rgb_uint >> 16) & 0xFF # shift by 16 bits and mask last 8 bits
g = (rgb_uint >> 8) & 0xFF # shift by 8 bits and mask last 8 bits
b = rgb_uint & 0xFF # mask last 8 bits

# Open3D wants float colours in range [0,1] so divide by 255 (2^8 -1)
colors = np.column_stack((r, g, b)).astype(np.float32) / 255.0

colors_arr = np.asarray(colors)  # values in [0, 1], shape (N, 3)
colors_hsv = cls.rgb_to_hsv(colors)

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)
pcd.colors = o3d.utility.Vector3dVector(colors)

# red hue is near 0.0 (or near 1.0, since hue wraps around)
mask = (
    (colors_hsv[:, 0] > 0.05) &   # orange hue lower bound
    (colors_hsv[:, 0] < 0.14) &   # orange hue upper bound
    (colors_hsv[:, 1] > 0.25) &   # reasonably saturated
    (colors_hsv[:, 2] > 0.20)     # not too dark
)
pegboard_masked_pcd = pcd.select_by_index(np.where(mask)[0])


#o3d.visualization.draw_geometries([pegboard_masked_pcd])

import open3d as o3d
import numpy as np


# Generated basic peg-transfer PointCloud using Open3D from .OBJ files and hard-coded positions in space

peg_board_location = '/home/dvrk-team/dvrk_ctrl_ws/src/peg_sim/ADF/Phantoms/Pegboards/high_res/peg_board.OBJ'


peg_board_mesh = o3d.io.read_triangle_mesh(peg_board_location)

peg_board_mesh.compute_vertex_normals()


peg_board_mesh.paint_uniform_color([1, 0, 0]) # paint peg_board red


peg_board_model_pcd = peg_board_mesh.sample_points_uniformly(number_of_points=10000) # sample points from mesh to point cloud

pcd_array = np.asarray(peg_board_model_pcd.points)

pcd_array[:,2] = 0 # flatten to 2D (remove z-points)

# Write back to Open3D point cloud
peg_board_model_pcd.points = o3d.utility.Vector3dVector(pcd_array)

# Visualize
#o3d.visualization.draw_geometries([peg_board_model_pcd])

# O3D helper function - apply transform on source pointcloud to visualise overlap with target
def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp])

# I have the peg_board object pointcloud = peg_board_model_pcd
# I have the the peg_board seen in the camera's frame = block_masked_pcd

# These are not aligned - each have their own origin positions and orientations

# I need to provide ICP with a simple starting point - the peg_board is approx here and facing this direction

# finds average of x, y, z points
position_guess = np.mean(np.asarray(pegboard_masked_pcd.points), axis=0)
rotation_guess = np.array([
    [1.0, 0.0, 0.0],
    [0.0, -0.45, -0.90],
    [0.0, 0.90, -0.45]
])

# rotation_guess = np.array([ # 180 deg
#     [1.0, 0.0, 0.0],
#     [0.0, -0.5984601,  0.8011526],
#     [0.0, -0.8011526, 0.5984601]
# ])


# returns 4x4 matrix with ones (1) on the diagonal and zeros (0) elsewhere
# appends first 3 rows of column 3 with x,y,z averages = transform matrix
init = np.eye(4)
init[:3, :3] = rotation_guess
init[:3, 3] = position_guess
# from scipy.spatial.transform import Rotation
# ro = Rotation.from_matrix(init[:3, :3])
# print(ro.as_euler('xyz', degrees=True))  # roll, pitch, yaw in degrees

"""""
[[ 1.          0.          0.         -0.14463816]
 [ 0.          1.          0.         -0.00501714]
 [ 0.          0.          1.         -0.03335711]
 [ 0.          0.          0.          1.        ]] """


peg_board_model_pcd.translate(-peg_board_model_pcd.get_center())
#print(peg_board_model_pcd.get_center())  # should now be ~[0,0,0]

pegboard_masked_pcd.estimate_normals()
peg_board_model_pcd.estimate_normals()

source = peg_board_model_pcd
target = pegboard_masked_pcd
result = o3d.pipelines.registration.registration_icp(
    source=source, 
    target=target,
    max_correspondence_distance=0.05,
    init=init,
    estimation_method=o3d.pipelines.registration.TransformationEstimationPointToPoint(),
    criteria=o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=100))

result2 = o3d.pipelines.registration.registration_icp(
    source=source, 
    target=target,
    max_correspondence_distance=0.001,
    init=result.transformation,
    estimation_method=o3d.pipelines.registration.TransformationEstimationPointToPoint(),
    criteria=o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=100))

pegboard_pose = result2.transformation
position_in_camera_frame = pegboard_pose[:3, 3]

# print("T_pegboard_in_camera: ", pegboard_pose)
#print("position in camera frame: ", position_in_camera_frame)


#draw_registration_result(peg_board_model_pcd, pegboard_masked_pcd, pegboard_pose)
#########################################BLOCK############################################################
# left stereo camera depth data from ROS topic /ambf/env/stereo/left/DepthData
data = np.load('/home/dvrk-team/internship/compvis/pointcloudL_new.npy') 

points = data[:, 0:3] # columns 0-2 (x, y, z)
rgb = data[:,3] # column 3 (rgb)

# reinterpret float32 bits as uint32
rgb_uint = rgb.view(np.uint32)

# extract rgb
# rrrrrrrr gggggggg bbbbbbbb
r = (rgb_uint >> 16) & 0xFF # shift by 16 bits and mask last 8 bits
g = (rgb_uint >> 8) & 0xFF # shift by 8 bits and mask last 8 bits
b = rgb_uint & 0xFF # mask last 8 bits

# Open3D wants float colours in range [0,1] so divide by 255 (2^8 -1)
colors = np.column_stack((r, g, b)).astype(np.float32) / 255.0

colors_arr = np.asarray(colors)  # values in [0, 1], shape (N, 3)
colors_hsv = cls.rgb_to_hsv(colors)

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)
pcd.colors = o3d.utility.Vector3dVector(colors)

# red hue is near 0.0 (or near 1.0, since hue wraps around)
mask = ((colors_hsv[:,0] < 0.02) | (colors_hsv[:,0] > 0.95)) & \
       (colors_hsv[:,1] > 0.3) & \
       (colors_hsv[:,2] > 0.2)


# mask = ( (colors_hsv[:,0] > 0.20)) & \ - ISOLATES BLUE BLOCK
#        (colors_hsv[:,1] > 0.3) & \
#        (colors_hsv[:,2] > 0.2)

# block_masked_pcd = pcd.select_by_index(np.where(mask)[0])

block_masked_pcd = pcd.select_by_index(np.where(mask)[0])

#o3d.visualization.draw_geometries([pcd])
# o3d.visualization.draw_geometries([block_masked_pcd])

# Generated basic peg-transfer PointCloud using Open3D from .OBJ files and hard-coded positions in space

block_location = '/home/dvrk-team/dvrk_ctrl_ws/src/peg_sim/ADF/Phantoms/Pegboards/high_res/block5.OBJ'


block_mesh = o3d.io.read_triangle_mesh(block_location)


#block_mesh.translate((0.024444686345014878, 0.2527384840964206, 0.7226560295887468),relative=False)


block_mesh.compute_vertex_normals()


block_mesh.paint_uniform_color([1, 0, 0]) # paint block red


block_model_pcd = block_mesh.sample_points_uniformly(number_of_points=5000) # sample points from mesh to point cloud


# o3d.visualization.draw_geometries([block_model_pcd]) #, peg_pcd, peg_board_pcd]) # visualize the point cloud and mesh together

# finds average of x, y, z points
position_guess = np.mean(np.asarray(block_masked_pcd.points), axis=0)

pegboard_rotation = pegboard_pose[0:3,0:3]
# print(f"pose: {pegboard_pose}")
# print(f"rotation: {pegboard_rotation}")

theta = np.radians(180)
R_90_z = np.array([
    [np.cos(theta), -np.sin(theta), 0],
    [np.sin(theta),  np.cos(theta), 0],
    [0,              0,             1]
])

# Matrix multiplication
rotation_guess = pegboard_rotation @ R_90_z 

# print(f"new rotation: {rotation_guess}")

#rotation_guess = 1 # CHANGE WITH PEGBOARD
# returns 4xnew 4 matrix with ones (1) on the diagonal and zeros (0) elsewhere
# appends first 3 rows of column 3 with x,y,z averages = transform matrix
init = np.eye(4)
init[:3, :3] = rotation_guess
init[:3, 3] = position_guess

"""""
[[ 1.          0.          0.         -0.14463816]
 [ 0.          1.          0.         -0.00501714]
 [ 0.          0.          1.         -0.03335711]
 [ 0.          0.          0.          1.        ]] """


block_model_pcd.translate(-block_model_pcd.get_center())
#print(block_model_pcd.get_center())  # should now be ~[0,0,0]

block_masked_pcd.estimate_normals()
block_model_pcd.estimate_normals()

source = block_model_pcd
target = block_masked_pcd
threshold = 0.02
result = o3d.pipelines.registration.registration_icp(
    source=source, 
    target=target,
    max_correspondence_distance=0.05,
    init=init,
    estimation_method=o3d.pipelines.registration.TransformationEstimationPointToPoint(),
      criteria=o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=100))

result2 = o3d.pipelines.registration.registration_icp(
    source=source, 
    target=target,
    max_correspondence_distance=0.001,
    init=result.transformation,
    estimation_method=o3d.pipelines.registration.TransformationEstimationPointToPoint(),
      criteria=o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=100))

final_pose = result2.transformation
position_in_camera_frame = final_pose[:3, 3]

#print(final_pose)
#print(position_in_camera_frame)


#draw_registration_result(block_model_pcd, block_masked_pcd, init)
draw_registration_result(block_model_pcd, block_masked_pcd, final_pose)

# def draw_multi(geometries_with_colors):
#     """
#     geometries_with_colors: list of (pointcloud, color, transform_or_None) tuples
#     """
#     to_draw = []
#     for pcd, color, transform in geometries_with_colors:
#         temp = copy.deepcopy(pcd)
#         temp.paint_uniform_color(color)
#         if transform is not None:
#             temp.transform(transform)
#         to_draw.append(temp)
#     o3d.visualization.draw_geometries(to_draw)

# draw_multi([
#     (block_model_pcd,    [1, 0.706, 0],   final_pose),      # orange = block model, aligned
#     (peg_board_model_pcd, [0, 1, 0],       pegboard_pose),   # green  = pegboard model, aligned
#     (block_masked_pcd,   [0, 0.651, 0.929], None),                # blue   = observed block points
#     (pegboard_masked_pcd,[0.7, 0.3, 0.9], None),                  # purple = observed pegboard points
# ])

# draw_multi()

# print(f"T_block in camera: {final_pose}")

######## THE BELOW MUST BE CONVERTED FROM CAMERA-L FRAME INTO THE BASE FRAME

############ FIXED ROTATION MATRIX APPLIED AS WAS 180 DISORIENTED
rotation_matrix = np.array([
    [-1.0, 0.0,  0.0],
    [ 0.0, 1.0,  0.0],
    [ 0.0, 0.0, -1.0]
])
rotation_fix = final_pose[0:3,0:3] @ rotation_matrix

# extract rotation matrix and convert into PyKDL.Rotation (3D array flattened into 1D)
#rot = PyKDL.Rotation(*final_pose[0:3,0:3].flatten())
rot = PyKDL.Rotation(*rotation_fix.flatten())
# convert to RPY 
roll, pitch, yaw = rot.GetRPY()
# print(f"roll: {roll}, pitch: {pitch}, yaw: {yaw}")

# extraction x,y,z and turn into PyKDL Vector
pos = PyKDL.Vector(*final_pose[0:3,3].flatten())
# print(f"position: {pos}")

block_in_cam = PyKDL.Frame(PyKDL.Rotation.RPY(roll, pitch, yaw), pos)
print(f"block pose in camL: {block_in_cam}")

##################################################################################################################
#------------------------- CLASS INSTANCES -------------------------#
rclpy.init()
object_pose_client = ObjectPoseClient() # Instance of service class
psm1 = ToolCommand('psm1')
psm2 = ToolCommand('psm2')
sim = SimControl()
init_handlers(object_pose_client) # pass client-side handler to routines,py

def run_task(parameters):
    params = parameters # parameters.yaml - offsets, objects etc.
    sim.reset_env() # Reset all simulation bodies (e.g. blocks, PSMs)
    time.sleep(2.0)
    PsmInit(psm=psm2, jp_init=params['init']['psm2_init'], jaw_init=params['init']['jaw_open'], max_wait=10)
    time.sleep(3.0)
    target_arm = psm2

    camframe_in_w = get_object_pose('cameraframe')
    #print(f'StereoL in World: {camframe_in_w}')

    stereoL_in_camera = get_object_pose('stereoL')
    #print(f'StereoL in CameraFrame: {stereoL_in_camera}')

    stereoL_in_w = camframe_in_w * stereoL_in_camera

    base_in_w = ps_to_frame(target_arm.T_b_w)
    #print(f"PSM2 base in World: {base_in_w}")

    block_in_world = stereoL_in_w * block_in_cam

    #block_in_base = base_in_w.Inverse() * stereoL_in_w * block_in_cam#base_in_w.Inverse() * stereoL_in_w * block_in_cam
    block_in_base = base_in_w.Inverse() * block_in_world
    print(f"Calculated Block in base: {block_in_base}")

    actual_block_in_w = get_object_pose('block5')
    actual_block_in_base = base_in_w.Inverse() * actual_block_in_w
    print(f"Actual Block in base: {actual_block_in_base}")

    T_ee_base = ps_to_frame(target_arm.measured_cp) # Grab ee relative to base pose from psm2/measured_cp and convert to frame
    T_ee_w = base_in_w * T_ee_base # ee in world is multiplication of previous transforms
    R_desired_w = T_ee_w.M # Target grasp orientation in world frame
    R_offset = (block_in_world.M).Inverse() * R_desired_w # Desired rotation offset converted to block frame

    enter_scene(target_arm)
    move = False

    local_offset = PyKDL.Frame(R_offset, PyKDL.Vector(-0.002,0.001, 0.05)) # compile local offset into a Frame
    
    target_pose = block_in_base * local_offset # apply local offset to target object in world = target

    psm_to_pose(psm=target_arm, target_pose=target_pose, success_flag=move) # grasp




def main():
    parameters = load_config()
    executor = MultiThreadedExecutor()
    executor.add_node(psm1)
    executor.add_node(psm2)
    executor.add_node(object_pose_client)
    executor.add_node(sim)
    
    spin_thread = threading.Thread(target=executor.spin, daemon=True)
    spin_thread.start()

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
    