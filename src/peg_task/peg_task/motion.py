# psm_to_block, path planning etc.

from PyKDL import Frame
import time

# Math Imports
from peg_math.conversions import ps_to_frame, rbs_to_frame
from peg_math.interpolation import cartesian_interpolate_step, cartesian_interpolate_step_new # Utility function that, given a current frame and a target frame, computes the next incremental step towards the target frame


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
        print(f"rotational error: {rot}, deadband: {rot_deadband}")
        #print(T_step)

        psm.servo_cp(T_step) # Set cartesian pose of servo
        time.sleep(control_speed) # Adjustable speed so can slow down more intricate movements (e.g. pick and place)