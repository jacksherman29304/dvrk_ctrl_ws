from PyKDL import Frame, Vector, Rotation
import numpy as np

from scipy.interpolate import CubicSpline

def cartesian_interpolate_step(T_curr, T_goal, max_delta=0.01, deadband=0.01):
    error = np.zeros(6)
    pe = T_goal.p - T_curr.p # pos error
    re = (T_curr.M.Inverse() * T_goal.M).GetRPY() # rotation error
    for i in range(6):
        if i < 3:
            error[i] = pe[i] # first 3 array points = x,y,z error
        else:
            error[i] = re[i-3] # final 3 array points = R,P,Y error

    done = False
    error_max = max(np.abs(error)) 
    if error_max <= deadband:
        error_scaled = error * 0.
        done = True
    else:
        error_scaled = error / error_max

    error_scaled = error_scaled * max_delta

    # T_step is a Frame(RPY, Vector(x,y,z))
    T_step = Frame(Rotation.RPY(error_scaled[3], error_scaled[4], error_scaled[5]),
                                Vector(error_scaled[0], error_scaled[1], error_scaled[2]))
    return T_step, done


def cartesian_interpolate_step_new(T_curr, T_goal, max_delta=0.01, pos_deadband=0.01, rot_deadband=0.01):
    error = np.zeros(6)
    pe = T_goal.p - T_curr.p # pos error
    re = (T_curr.M.Inverse() * T_goal.M).GetRPY() # rotation error
    for i in range(6):
        if i < 3:
            error[i] = pe[i] # first 3 array points = x,y,z error
        else:
            error[i] = re[i-3] # final 3 array points = R,P,Y error

    rot_done = False
    pos_done = False
    done = False
    error_max = max(np.abs(error)) 

    rot_error_max = max(np.abs(error[3:6]))
    pos_error_max = max(np.abs(error[0:3])) 

    if rot_error_max <= rot_deadband:
        rot_error_scaled = np.zeros(3)
        rot_done = True
    else:
        rot_error_scaled = (error[3:6] / error_max) * max_delta

    if pos_error_max <= pos_deadband:
       pos_error_scaled = np.zeros(3)
       pos_done = True
       
    else:
        pos_error_scaled = (error[0:3] / error_max) * max_delta

    done = rot_done and pos_done         

    # T_step is a Frame(RPY, Vector(x,y,z))
    T_step = Frame(Rotation.RPY(rot_error_scaled[0], rot_error_scaled[1], rot_error_scaled[2]),
                                Vector(pos_error_scaled[0], pos_error_scaled[1], pos_error_scaled[2]))
    return T_step, done


# def pos_spline(T_curr, T_goal):
#     x_current = T_curr.p.x
#     y_current = T_curr.p.y
#     z_current = T_curr.p.z

#     x_new = T_goal.p.x
#     y_new = T_goal.p.y
#     z_new = T_goal.p.z

#     cs_x = CubicSpline()