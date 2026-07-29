# psm_to_block, path planning etc.

from PyKDL import Frame
import time

import csv, os

# Math Imports
from peg_math.conversions import ps_to_frame, rbs_to_frame
from peg_math.interpolation import cartesian_interpolate_step, cartesian_interpolate_step_new # Utility function that, given a current frame and a target frame, computes the next incremental step towards the target frame


# #------------------------- CONTROL FUNCTIONS  -------------------------#

# def psm_to_pose(psm, target_pose: Frame, success_flag: bool, control_speed=0.01, max_delta=0.01, pos_deadband=0.005, rot_deadband=0.01, timeout=15.0, log_path=None):
#     success_flag = False
#     start = time.time()
#     while not success_flag:

#         if (time.time() - start) < timeout:

#             T_current = ps_to_frame(psm.measured_cp)

            
#             T_delta, success_flag = cartesian_interpolate_step_new(T_current, target_pose, max_delta, pos_deadband=pos_deadband,rot_deadband=rot_deadband)

#             T_step = Frame() # New command frame that adds positional and rotational delta to current tool position
#             T_step.p = T_current.p + T_delta.p # step positin = current position + delta position
#             T_step.M = T_current.M * T_delta.M # step rotation = current rotation * delta rotation

            
#             dist = (target_pose.p - T_current.p).Norm()
#             rot = (T_current.M.Inverse() * target_pose.M).GetRPY()
#             print(f"dist to target: {dist:.5f}, deadband: {pos_deadband}")
#             print(f"rotational error: {rot}, deadband: {rot_deadband}")


#             psm.servo_cp(T_step) # Set cartesian pose of servo
#             time.sleep(control_speed) # Adjustable speed so can slow down more intricate movements (e.g. pick and place)



#         else:
#             print(f"ERROR:psm_to_pose exceeded {timeout}s")
#             break





def psm_to_pose(psm, target_pose: Frame, success_flag: bool, control_speed=0.01, max_delta=0.01, pos_deadband=0.005, rot_deadband=0.01, timeout=30.0, log=False):

    success_flag = False
    t0 = time.time()
    roll_error_log = []
    pitch_error_log = []
    yaw_error_log = []
    dist_error_log = []

    while not success_flag:

        if (time.time() - t0) >= timeout:
            print(f"ERROR:psm_to_pose exceeded {timeout}s") # if doesn't converge after set timeout, breaks out of loop
            break


        T_current = ps_to_frame(psm.measured_cp)

            
        T_delta, success_flag = cartesian_interpolate_step_new(T_current, target_pose, max_delta, pos_deadband=pos_deadband,rot_deadband=rot_deadband)

        T_step = Frame() # New command frame that adds positional and rotational delta to current tool position
        T_step.p = T_current.p + T_delta.p # step positin = current position + delta position
        T_step.M = T_current.M * T_delta.M # step rotation = current rotation * delta rotation

            
        dist_error_norm = (target_pose.p - T_current.p).Norm()
        rpy_error = (T_current.M.Inverse() * target_pose.M).GetRPY()

        roll_error_log.append(rpy_error[0])
        pitch_error_log.append(rpy_error[1])
        yaw_error_log.append(rpy_error[2])

        dist_error_log.append(dist_error_norm)


        psm.servo_cp(T_step) # Set cartesian pose of servo
        time.sleep(control_speed) # Adjustable speed so can slow down more intricate movements (e.g. pick and place)

    if log:
        return dist_error_log, roll_error_log, pitch_error_log, yaw_error_log
    else:
        return



# def psm_to_pose(psm, target_pose: Frame, success_flag: bool, control_speed=0.01, max_delta=0.01, pos_deadband=0.005, rot_deadband=0.01, log_path=None):
#     success_flag = False
#     t0 = time.time()

#     f = writer = None
#     if log_path is not None:
#         os.makedirs(os.path.dirname(log_path), exist_ok=True)
#         f = open(log_path, 'w', newline='')
#         writer = csv.writer(f)
#         writer.writerow(['t', 'roll', 'pitch', 'yaw', 'dist'])
#         print(f"logging to {log_path}")

#     try:
#         while not success_flag:
#             T_current = ps_to_frame(psm.measured_cp)
#             T_delta, success_flag = cartesian_interpolate_step_new(T_current, target_pose, max_delta, pos_deadband=pos_deadband, rot_deadband=rot_deadband)

#             T_step = Frame()
#             T_step.p = T_current.p + T_delta.p
#             T_step.M = T_current.M * T_delta.M

#             dist = (target_pose.p - T_current.p).Norm()
#             rot = (T_current.M.Inverse() * target_pose.M).GetRPY()
#             print(f"dist to target: {dist:.5f}, deadband: {pos_deadband}")
#             print(f"rotational error: {rot}, deadband: {rot_deadband}")

#             if writer is not None:
#                 writer.writerow((time.time() - t0, rot[0], rot[1], rot[2], dist))
#                 f.flush()

#             psm.servo_cp(T_step)
#             time.sleep(control_speed)
#     finally:
#         if f is not None:
#             f.close()


# def psm_to_pose(psm, target_pose: Frame, success_flag: bool, control_speed=0.01,
#                 max_delta=0.01, pos_deadband=0.005, rot_deadband=0.01):
#     success_flag = False
#     T_cmd = ps_to_frame(psm.measured_cp)          # seed ONCE, outside the loop

#     while not success_flag:
#         T_current = ps_to_frame(psm.measured_cp)  # feedback — unchanged
#         T_delta, success_flag = cartesian_interpolate_step_new(
#             T_current, target_pose, max_delta,
#             pos_deadband=pos_deadband, rot_deadband=rot_deadband)

#         # advance the COMMAND, not the measured pose
#         T_cmd = Frame(T_cmd.M * T_delta.M, T_cmd.p + T_delta.p)

#         psm.servo_cp(T_cmd)
#         time.sleep(control_speed)

# def psm_to_pose(psm, target_pose: Frame, success_flag: bool, control_speed=0.01,
#                 max_delta=0.01, pos_deadband=0.005, rot_deadband=0.01):
#     T_cmd = ps_to_frame(psm.measured_cp)   # seed once
#     arrived = False

#     while not arrived:
#         # 1. advance the COMMAND toward the TARGET (feedforward trajectory)
#         T_delta, _ = cartesian_interpolate_step_new(
#             T_cmd, target_pose, max_delta,
#             pos_deadband=pos_deadband, rot_deadband=rot_deadband)
#         T_cmd = Frame(T_cmd.M * T_delta.M, T_cmd.p + T_delta.p)
#         psm.servo_cp(T_cmd)

#         # 2. exit only when the ARM has actually got there
#         T_current = ps_to_frame(psm.measured_cp)
#         _, arrived = cartesian_interpolate_step_new(
#             T_current, target_pose, max_delta,
#             pos_deadband=pos_deadband, rot_deadband=rot_deadband)

#         time.sleep(control_speed)