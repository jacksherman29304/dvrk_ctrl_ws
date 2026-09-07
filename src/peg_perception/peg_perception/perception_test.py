import rclpy
from rclpy.node import Node
import threading
from rclpy.executors import MultiThreadedExecutor
from PyKDL import Frame, Vector, Rotation


from peg_perception.camera_interface import CameraInterface
from peg_perception.pcd_processing import block_in_cam
from peg_task.ros_interface import ObjectPoseClient, SimControl
from peg_task.routines import get_object_pose, init_handlers

from pathlib import Path
import numpy as np
import itertools
import time
import json
import csv

#------------------------- VARIABLES -------------------------#

# J3_DEPTH_OFFSET = {
#     "near" : +0.01,
#     "mid": 0.00,
#     "far": -0.01
# }

# J1_ANGLE_OFFSET = {
#     "L": -0.02,
#     "R": +0.02
# }

# J2_ANGLE_OFFSET = {
#     "L": -0.02,
#     "R": +0.02
# }

## best so far
# J3_DEPTH_OFFSET = {
#     "near" : +0.03,
#     "mid": 0.00,
#     "far": -0.01
# }

# J1_ANGLE_OFFSET = {
#     "L": -0.02,
#     "R": +0.02
# }

# J2_ANGLE_OFFSET = {
#     "L": -0.02,
#     "R": +0.02
# }

## best best so far
J3_DEPTH_OFFSET = {
    "near" : +0.005,
    "mid": 0.00,
    "far": -0.005
}

J1_ANGLE_OFFSET = {
    "L": -0.001,
    "R": +0.001
}

J2_ANGLE_OFFSET = {
    "L": -0.001,
    "R": +0.001
}

J4_ANGLE_OFFSET = 0.00

# OUTPUT_PATH = Path('/home/dvrk-team/Desktop/perception_test_capture')

#------------------------- CLASS INSTANCES -------------------------#
rclpy.init()
camera_interface = CameraInterface()
object_pose_client = ObjectPoseClient()
sim = SimControl()
init_handlers(object_pose_client) # pass client-side handler to routines,py
OUTPUT_DIR = Path('/home/dvrk-team/Desktop/perception_test_capture')
TARGET_OBJECT_NAME = 'block5'

#------------------------- HELPERS -------------------------#
def pykdl_frame_to_dict(frame):
    p = frame.p
    rpy = frame.M.GetRPY()
    return {
        'position': [p.x(), p.y(), p.z()],
        'rpy': list(rpy),
    }


def pos_error(ref_pose: Frame, calc_pose: Frame):
    ref_x = ref_pose.p.x()
    ref_y = ref_pose.p.y()
    ref_z = ref_pose.p.z()

    ref = np.array([ref_x, ref_y, ref_z])

    calc_x = calc_pose.p.x()
    calc_y = calc_pose.p.y()
    calc_z = calc_pose.p.z()

    calc = np.array([calc_x, calc_y, calc_z])

    pos_error = np.linalg.norm(calc-ref)

    return pos_error


def ang_error(ref_pose: Frame, calc_pose: Frame):
    ref_quat = np.array((ref_pose.M).GetQuaternion())
    calc_quat = np.array((calc_pose.M).GetQuaternion())

    dot = np.clip(abs(np.dot(calc_quat, ref_quat)), -1.0, 1.0)
    angle_rad = 2 * np.arccos(dot)

    return np.degrees(angle_rad)

#------------------------- COLLECT PCDs -------------------------#
def collect_pcd():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    i = 0
    poses = []
    measured_base_js = camera_interface.get_js() # baseline ECM jp
    base_js = list(measured_base_js.position)

    for (depth_label, dj3), (j1_label, dj1), (j2_label, dj2) in itertools.product(
        J3_DEPTH_OFFSET.items(), J1_ANGLE_OFFSET.items(), J2_ANGLE_OFFSET.items()
    ):
        target = [
            base_js[0] + dj1,
            base_js[1] + dj2,
            base_js[2] + dj3,
            base_js[3] + J4_ANGLE_OFFSET,
        ]
        label = f'd{depth_label}_j1{j1_label}_j2{j2_label}'
        poses.append((label, target))



    csv_path = OUTPUT_DIR / 'capture_log.csv'
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'label', 'pcd_file', 'meta_file',
            'j0_target', 'j1_target', 'j2_target', 'j3_target',
             'pos_error', 'ang_error'
        ])



        for label, target in poses:
            camera_interface.servo_jp(target)
            time.sleep(2.0)
 
            measured_js = list(camera_interface.get_js().position)            
 
            pcd_path = OUTPUT_DIR / f'pcd_{label}.pcd'
            meta_path = OUTPUT_DIR / f'meta_{label}.json'

            npy_path = Path(str(pcd_path) + '.npy')

 
            camera_interface.save_left_pcd(pcd_path)
            
            t0 = time.time()
            while not npy_path.exists() and time.time() - t0 < 5.0:
                time.sleep(0.05)


             # ground truth: query AMBF directly, not via FK from joint states
            camframe_in_w = get_object_pose('cameraframe')
            stereoL_in_camera = get_object_pose('stereoL')
            stereoL_in_w = camframe_in_w * stereoL_in_camera
            reference_in_w = get_object_pose(TARGET_OBJECT_NAME) # known ground truth from ambf



            target_in_cam = block_in_cam(npy_path) # calculated from pcd
            target_in_w = stereoL_in_w * target_in_cam

            print(f"Calculated block in World: {target_in_w}")
            print(f"Actual block in World: {reference_in_w}")

            position_error = pos_error(ref_pose=reference_in_w, calc_pose=target_in_w) # euclidain error (m)
            angular_error = ang_error(ref_pose=reference_in_w, calc_pose=target_in_w) # geosidic (angular) error (deg) - (0deg = identical, 180deg = max error)

            # meta = {
            #     'label': label,
            #     'joint_target': target,
            #     'joint_measured': measured_js,
            #     'stereoL_in_world': pykdl_frame_to_dict(stereoL_in_w),
            #     'reference_in_world': pykdl_frame_to_dict(reference_in_w),
            #     'target_in_world': pykdl_frame_to_dict(target_in_w),
            # }
            # meta_path.write_text(json.dumps(meta, indent=2))

 
            writer.writerow([
                label, pcd_path.name, meta_path.name,
                *target, position_error, angular_error
            ])
            csvfile.flush()
            # print(f'Saved {pcd_path.name} + {meta_path.name}')
            print(f'Saved {pcd_path.name}')
 

#------------------------- MAIN -------------------------#
def main():
    executor = MultiThreadedExecutor()
    executor.add_node(camera_interface)
    executor.add_node(object_pose_client)

    
    spin_thread = threading.Thread(target=executor.spin, daemon=True)
    spin_thread.start()

    try:
        sim.reset_env() # Reset all simulation bodies (e.g. blocks, PSMs)
        time.sleep(3.0)
        object_pose_client.wait_for_server()
        collect_pcd()
        
            
    finally:
        executor.shutdown()
        spin_thread.join(timeout=2.0)
        camera_interface.destroy_node()
        object_pose_client.destroy_node()
        sim.destroy_node()
        rclpy.shutdown()

# anything in here is invisivle to ros2 run
if __name__ == '__main__':
    main()
    