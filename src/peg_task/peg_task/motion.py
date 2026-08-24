# psm_to_block, path planning etc.

from PyKDL import Frame
import time
import matplotlib.pyplot as plt
import numpy as np
import inspect
import csv, os

# Math Imports
from peg_helpers.conversions import ps_to_frame
from peg_helpers.interpolation import cartesian_interpolate_step_new # Utility function that, given a current frame and a target frame, computes the next incremental step towards the target frame
from peg_helpers.testers import PSMTimeoutError

def psm_to_pose(psm, target_pose: Frame, success_flag: bool, control_speed=0.01, max_delta=0.01, pos_deadband=0.005, rot_deadband=0.01, timeout=30.0, log=False):

    success_flag = False
    t0 = time.time()
    roll_error_log = []
    pitch_error_log = []
    yaw_error_log = []
    dist_error_log = []
    distance_travelled = 0

    while not success_flag:

        if (time.time() - t0) >= timeout:
            # print(f"ERROR:psm_to_pose exceeded {timeout}s") # if doesn't converge after set timeout, breaks out of loop

            stack = inspect.stack() # return list of data about call stack
            failure_stage = stack[2].function # looking up 2-levels at the executing function (psm_to_pose -> gripper_to_pose -> executing_routine)
            
            print(f"ERROR:psm_to_pose exceeded {timeout}s in stage: {failure_stage}")
            raise PSMTimeoutError(failure_stage=failure_stage) # update failure_stage in exception class
           


        T_current = ps_to_frame(psm.measured_cp)

            
        T_delta, success_flag = cartesian_interpolate_step_new(T_current, target_pose, max_delta, pos_deadband=pos_deadband,rot_deadband=rot_deadband)

        T_step = Frame() # New command frame that adds positional and rotational delta to current tool position
        T_step.p = T_current.p + T_delta.p # step positin = current position + delta position
        T_step.M = T_current.M * T_delta.M # step rotation = current rotation * delta rotation

        distance_travelled += T_delta.p.Norm() # euclidian distance travelled = sqrt(x2 + y2 + z2)


        # dist_error_norm = (target_pose.p - T_current.p).Norm()
        # rpy_error = (T_current.M.Inverse() * target_pose.M).GetRPY()

        # roll_error_log.append(rpy_error[0])
        # pitch_error_log.append(rpy_error[1])
        # yaw_error_log.append(rpy_error[2])

        # dist_error_log.append(dist_error_norm)


        psm.servo_cp(T_step) # Set cartesian pose of servo
        time.sleep(control_speed) # Adjustable speed so can slow down more intricate movements (e.g. pick and place)


    if log:
        return #dist_error_log, roll_error_log, pitch_error_log, yaw_error_log
    else:
        return distance_travelled


# Trajectory plotting variant of psm_to_pose
def psm_to_pose_plot(psm, target_pose: Frame, success_flag: bool, control_speed=0.01, max_delta=0.01, pos_deadband=0.005, rot_deadband=0.01, timeout=30.0):

    success_flag = False
    t0 = time.time()
    x_log = []
    y_log = []
    z_log = []
    yaw_log = []

    while not success_flag:

        if (time.time() - t0) >= timeout:
            print(f"ERROR:psm_to_pose exceeded {timeout}s") # if doesn't converge after set timeout, breaks out of loop
            break


        T_current = ps_to_frame(psm.measured_cp)

        x_log.append(T_current.p.x())
        y_log.append(T_current.p.y())
        z_log.append(T_current.p.z())
        yaw_log.append(T_current.M.GetRPY()[2])

            
        T_delta, success_flag = cartesian_interpolate_step_new(T_current, target_pose, max_delta, pos_deadband=pos_deadband,rot_deadband=rot_deadband)

        T_step = Frame() # New command frame that adds positional and rotational delta to current tool position
        T_step.p = T_current.p + T_delta.p # step positin = current position + delta position
        T_step.M = T_current.M * T_delta.M # step rotation = current rotation * delta rotation


        psm.servo_cp(T_step) # Set cartesian pose of servo
        time.sleep(control_speed) # Adjustable speed so can slow down more intricate movements (e.g. pick and place)
    plot_trajectory(x_log, y_log, z_log)

 
def plot_trajectory(x_log, y_log, z_log, arrow_len=0.003):

    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    ax.plot(x_log, y_log, z_log, marker = 'o', color='g')
    #ax.scatter(*points.T[0], color = 'red')
    plt.show()