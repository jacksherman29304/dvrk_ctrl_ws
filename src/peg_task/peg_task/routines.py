# psm init, locate block etc.
 
import time
import numpy as np
from PyKDL import Vector, Frame, Rotation

from peg_math.conversions import ps_to_frame, rbs_to_frame
from peg_task.config import load_config
from peg_task.motion import psm_to_pose, psm_to_pose_plot

#------------------------- GLOBALS -------------------------#
_object_pose_client = None
_R_offset = None
#------------------------- NODE HANDLERS -------------------------#


# Get client-side handler for 'GetObjectPose' - eventually to be replaced with perception layer
def init_handlers(object_pose_client):
    global _object_pose_client
    _object_pose_client = object_pose_client


parameters = load_config()
global _get_parameter
_get_parameter = parameters 

#------------------------- PSM INIT -------------------------#
# Check CRTK BASED CONTROL SCRIPT AND ALSO ORIGINAL PEG TRANSFER
def PsmInit(psm, jp_init, jaw_init, max_wait):

    psm.move_jp(jp_init)
    psm.set_jaw(jaw_init)

    # Timer added to allow PSMs to reach initialised joint positions before measuring frames - prevents inaccurate early readings
    start = time.time() # starts timer for elapsed time
    while time.time() - start < max_wait: # whilst under max wait time in seconds

        js = psm.measured_js # measure current joint state of psm

        # current_jp becomes measured joint state if measured js is not empty and has at least 1 value
        current_jp = js.position if js is not None and len(js.position) > 0 else None 

        # if updated current_jp has read valid data and this joint position is within 0.005 tolerance of target joint position, break loop and enable frame readings
        if current_jp is not None and np.allclose(current_jp, jp_init, atol=0.005):
            break
        time.sleep(0.002)
    else: # error detection
        print(f"WARNING: {psm} did not converge to init position within {max_wait}s timeout")

#-------------------------  GET OBJECT POSE -------------------------#
# eventually remove pose_client
def get_object_pose(target_obj):
    object_pose = rbs_to_frame(_object_pose_client.get_object_pose(target_obj)) # target object in world (Frame)

    return object_pose

#------------------------- SUB-ROUTINES -------------------------#

# commanding gripper to certain pose
def move_gripper_to_pose(psm, target_object, rot_offset, pos_offset, max_delta, pos_deadband, rot_deadband):

    base_w = ps_to_frame(psm.T_b_w) # base in world pose, convert to Frame

    object_w = get_object_pose(target_object) # get target object pose in world

    local_offset = Frame(rot_offset, pos_offset) # compile local offset into a Frame

    target_pose_w = object_w * local_offset # apply local offset to target object in world = target final pose

    target_pose_b = base_w.Inverse() * target_pose_w # convert target object with offset in world into the base frame for PSM commands

    success_flag = False
    psm_to_pose(psm=psm, target_pose=target_pose_b, success_flag=success_flag, 
                max_delta=max_delta, pos_deadband=pos_deadband, rot_deadband=rot_deadband)

# commanding gripper with grasped item to certain pose
def move_grasped_object_to_pose(psm, grasped_object, rot_offset, pos_offset, max_delta, pos_deadband, rot_deadband,target_object=None, target_pose=None):

    base_w = ps_to_frame(psm.T_b_w) # base in world pose, convert to Frame

    ee_base = ps_to_frame(psm.measured_cp) # end-effector in base pose, converted to Frame

    ee_w = base_w * ee_base # end-effector in world

    object_w = get_object_pose(grasped_object) # get grasped object pose in world

    object_ee = ee_w.Inverse() * object_w # block in end-effector (grasp relationship)

    local_offset = Frame(rot_offset, pos_offset) # compile local offset into a Frame

    if target_pose is None:

        target_pose_w = get_object_pose(target_object) * local_offset # apply local offset to target object in world = target final pose

        target_pose_grasp_w = target_pose_w * object_ee.Inverse() # target final pose with grasp offset applied

        target_pose_b = base_w.Inverse() * target_pose_grasp_w # convert target object with offset in world into the base frame for PSM commands

    else:
        target_pose_b = target_pose

    success_flag = False
    psm_to_pose(psm=psm, target_pose=target_pose_b, success_flag=success_flag, 
                max_delta=max_delta, pos_deadband=pos_deadband, rot_deadband=rot_deadband)


#------------------------- TASK ROUTINES -------------------------#


def enter_scene(psm, target_block):
    T_base_w = ps_to_frame(psm.T_b_w) # Grab base in world pose from psm2/T_b_w and convert to frame
    T_ee_base = ps_to_frame(psm.measured_cp) # Grab ee relative to base pose from psm2/measured_cp and convert to frame
    T_ee_w = T_base_w * T_ee_base # ee in world is multiplication of previous transforms

    T_block_w = get_object_pose(target_block)

    R_desired_w = T_ee_w.M # Target grasp orientation in world frame

    global _R_offset

    _R_offset = (T_block_w.M).Inverse() * R_desired_w # Desired rotation offset converted to block frame

    if psm.get_tool_name() == "psm2":
        pos_offset = Vector(*_get_parameter['psm2_entrance']['pos_offset']) # approach from rhs
    else: 
        pos_offset = Vector(*_get_parameter['psm1_entrance']['pos_offset']) # approach from lhs

    print(f"Entering scene for {target_block}")

    move_gripper_to_pose(psm=psm, 
                    target_object=target_block, 
                    rot_offset= _R_offset, 
                    pos_offset= pos_offset,#pos_offset, 
                    max_delta=_get_parameter['psm1_entrance']['max_delta'], 
                    pos_deadband=_get_parameter['psm1_entrance']['pos_deadband'], 
                    rot_deadband=_get_parameter['psm1_entrance']['rot_deadband'])

    print("Entered Scene")

    time.sleep(1.0)

def grasp_block(psm, target_block):

    print(f"Moving to grasp {target_block}")

    if psm.get_tool_name()== "psm2":
        pos_offset = Vector(*_get_parameter['psm2_grasp']['pos_offset']) # approach from rhs
    else: 
        pos_offset = Vector(*_get_parameter['psm1_grasp']['pos_offset']) # approach from lhs

    move_gripper_to_pose(psm=psm,
                    target_object=target_block,
                    rot_offset = _R_offset,
                    pos_offset= pos_offset,
                    max_delta=_get_parameter['psm1_grasp']['max_delta'], # these metrics are common amongs L + R grips
                    pos_deadband=_get_parameter['psm1_grasp']['pos_deadband'], 
                    rot_deadband=_get_parameter['psm1_grasp']['rot_deadband'])

    print(f'Arrived at {target_block}')

    time.sleep(1.0)

    for _ in range(20):
        psm.set_jaw(0.04)
        time.sleep(0.05)

    print(f'Grasped {target_block}')

def lift_block(psm, target_block):

    print(f"Lifting {target_block}")

    move_grasped_object_to_pose(psm=psm,
                                grasped_object=target_block,
                                target_object=target_block,
                                rot_offset = Rotation.RPY(*_get_parameter['lift']['rot_offset']),
                                pos_offset = Vector(*_get_parameter['lift']['pos_offset']),
                                max_delta=_get_parameter['lift']['max_delta'], 
                                pos_deadband=_get_parameter['lift']['pos_deadband'], 
                                rot_deadband=_get_parameter['lift']['rot_deadband'])

    print(f"Lifted {target_block}")

    time.sleep(1.0)
    
def relocate_block(psm, target_block, target_peg):

    print(f"Relocating {target_block} to {target_peg}")

    move_grasped_object_to_pose(psm=psm,
                                grasped_object=target_block,
                                target_object=target_peg,
                                rot_offset = Rotation.RPY(*_get_parameter['relocate']['rot_offset']),
                                pos_offset = Vector(*_get_parameter['relocate']['pos_offset']),
                                max_delta=_get_parameter['relocate']['max_delta'], 
                                pos_deadband=_get_parameter['relocate']['pos_deadband'], 
                                rot_deadband=_get_parameter['relocate']['rot_deadband'])

    print(f"Relocated {target_block} to {target_peg}")

    time.sleep(1.0)

    
def place_block(psm, target_block, target_peg): # need to think about L + R variances

    print(f'Placing {target_block} on {target_peg}')

    if psm.get_tool_name()== "psm2":
        rot_offset = Rotation.RPY(*_get_parameter['psm2_place']['rot_offset']) # fix this 
    else: 
        rot_offset = Rotation.RPY(*_get_parameter['psm1_place']['rot_offset'])

    move_grasped_object_to_pose(psm=psm,
                                grasped_object=target_block,
                                target_object=target_peg,
                                rot_offset = rot_offset, 
                                pos_offset = Vector(*_get_parameter['psm1_place']['pos_offset']),
                                max_delta=_get_parameter['psm1_place']['max_delta'], 
                                pos_deadband=_get_parameter['psm1_place']['pos_deadband'], 
                                rot_deadband=_get_parameter['psm1_place']['rot_deadband'])

    psm.set_jaw(0.08)

    print(f"Placed {target_block} on {target_peg}")

    time.sleep(1.0)


def block_passover(psm, target_block): # split into 2 movements - some reason when PSM2 is grasping there is a rotation error

    if psm.get_tool_name()== "psm2": # incoming arm is psm2 (right-hand), so this would be left-to-right passover
        pos1_offset = Vector(*_get_parameter['1to2_passover']['pos_offset'])
    else:             # incoming arm is psm1 (left-hand), so this would be right-to-left passover
        pos1_offset = Vector(*_get_parameter['2to1_passover']['pos_offset'])

    print(f'secondary PSM entering scene')

    move_gripper_to_pose(psm=psm, 
                    target_object=target_block, 
                    rot_offset= _R_offset, 
                    pos_offset=pos1_offset, 
                    max_delta=_get_parameter['1to2_passover']['max_delta'], 
                    pos_deadband=_get_parameter['1to2_passover']['pos_deadband'], 
                    rot_deadband=_get_parameter['1to2_passover']['rot_deadband'])

    print(f"Secondary PSM entered scene")
    time.sleep(1.0)
    print(f"Secondary PSM grasping block")

    if psm.get_tool_name()== "psm2": # incoming arm is psm2 (right-hand), so this would be left-to-right passover
        pos2_offset = Vector(*_get_parameter['psm2_grasp']['pos_offset'])
    else:             # incoming arm is psm1 (left-hand), so this would be right-to-left passover
        pos2_offset = Vector(*_get_parameter['psm1_grasp']['pos_offset'])


    move_gripper_to_pose(psm=psm,
                    target_object=target_block,
                    rot_offset = _R_offset,
                    pos_offset= pos2_offset,
                    max_delta=_get_parameter['psm2_grasp']['max_delta'], 
                    pos_deadband=_get_parameter['psm2_grasp']['pos_deadband'], 
                    rot_deadband=_get_parameter['psm2_grasp']['rot_deadband'])

    for _ in range(20):
        psm.set_jaw(0.02)
        time.sleep(0.05)

    print(f"Secondary PSM grasped block")
    time.sleep(1.0)

def passover(grasp_psm, passover_psm, target_block='block5'):

    grasp_base_w = ps_to_frame(grasp_psm.T_b_w)
    grasp_ee_base = ps_to_frame(grasp_psm.measured_cp) # grasping psm pose in base
    grasp_ee_w = grasp_base_w * grasp_ee_base


    passover_base_w = ps_to_frame(passover_psm.T_b_w)
    passover_ee_base = ps_to_frame(passover_psm.measured_cp) # grasping psm pose in base
    passover_ee_w = passover_base_w * passover_ee_base
   
    # find midpoint between grippers in world
    # only vary x and y as height of gripper with block (z) should stay consistent
    
    #print(f"original grasp pose: {grasp_psm_pose}")

    # Calculated in world frame
    gx, gy, gz = grasp_ee_w.p
    px, py, pz = passover_ee_w.p

    mid_x = (gx + px)/2
    mid_y = (gy + py)/2

    grasp_ee_base.p[0] = mid_x
    grasp_ee_base.p[1] = mid_y

    midpoint_target_w = Frame(grasp_ee_w.M, Vector(mid_x, mid_y, gz))
    midpoint_target_base = grasp_base_w.Inverse() * midpoint_target_w # convert back to base frame

    #print(f"midway grasp pose: {grasp_psm_pose}")

    move_grasped_object_to_pose(psm=grasp_psm,
                                   grasped_object=target_block,
                                   target_pose = midpoint_target_base,
                                   rot_offset = Rotation.RPY(*_get_parameter['relocate']['rot_offset']), # currently zero
                                   pos_offset = Vector(*_get_parameter['psm1_place']['pos_offset']),
                                   max_delta=_get_parameter['relocate']['max_delta'], 
                                   pos_deadband=_get_parameter['relocate']['pos_deadband'], 
                                   rot_deadband=_get_parameter['relocate']['rot_deadband'])


    block_passover(passover_psm, target_block)
    time.sleep(1.0)