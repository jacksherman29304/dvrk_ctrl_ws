# psm init, locate block etc.
 
import time
import numpy as np
from PyKDL import Vector, Frame, Rotation

from peg_math.conversions import ps_to_frame, rbs_to_frame
from peg_task.config import load_config
from peg_task.motion import psm_to_pose

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
def move_grasped_object_to_pose(psm, grasped_object, target_object, rot_offset, pos_offset, max_delta, pos_deadband, rot_deadband):

    base_w = ps_to_frame(psm.T_b_w) # base in world pose, convert to Frame

    ee_base = ps_to_frame(psm.measured_cp) # end-effector in base pose, converted to Frame

    ee_w = base_w * ee_base # end-effector in world

    object_w = get_object_pose(grasped_object) # get grasped object pose in world

    object_ee = ee_w.Inverse() * object_w # block in end-effector (grasp relationship)

    local_offset = Frame(rot_offset, pos_offset) # compile local offset into a Frame

    target_pose_w = get_object_pose(target_object) * local_offset # apply local offset to target object in world = target final pose

    target_pose_grasp_w = target_pose_w * object_ee.Inverse() # target final pose with grasp offset applied

    target_pose_b = base_w.Inverse() * target_pose_grasp_w # convert target object with offset in world into the base frame for PSM commands

    success_flag = False
    psm_to_pose(psm=psm, target_pose=target_pose_b, success_flag=success_flag, 
                max_delta=max_delta, pos_deadband=pos_deadband, rot_deadband=rot_deadband)


#------------------------- TASK ROUTINES -------------------------#


def enter_scene(psm):
    T_base_w = ps_to_frame(psm.T_b_w) # Grab base in world pose from psm2/T_b_w and convert to frame
    T_ee_base = ps_to_frame(psm.measured_cp) # Grab ee relative to base pose from psm2/measured_cp and convert to frame
    T_ee_w = T_base_w * T_ee_base # ee in world is multiplication of previous transforms

    T_block_w = get_object_pose(_get_parameter['target_block'])

    R_desired_w = T_ee_w.M # Target grasp orientation in world frame

    global _R_offset

    _R_offset = (T_block_w.M).Inverse() * R_desired_w # Desired rotation offset converted to block frame

    print(f"Entering scene for {_get_parameter['target_block']}")

    move_gripper_to_pose(psm=psm, 
                    target_object=_get_parameter['target_block'], 
                    rot_offset= _R_offset, 
                    pos_offset=Vector(*_get_parameter['entrance']['pos_offset']), 
                    max_delta=_get_parameter['entrance']['max_delta'], 
                    pos_deadband=_get_parameter['entrance']['pos_deadband'], 
                    rot_deadband=_get_parameter['entrance']['rot_deadband'])

    print("Entered Scene")

    time.sleep(2.0)

def grasp_block(psm):

    print(f"Moving to grasp {_get_parameter['target_block']}")

    move_gripper_to_pose(psm=psm,
                    target_object=_get_parameter['target_block'],
                    rot_offset = _R_offset,
                    pos_offset= Vector(*_get_parameter['grasp']['pos_offset']),
                    max_delta=_get_parameter['grasp']['max_delta'], 
                    pos_deadband=_get_parameter['grasp']['pos_deadband'], 
                    rot_deadband=_get_parameter['grasp']['rot_deadband'])

    print(f'Arrived at {_get_parameter['target_block']}')

    time.sleep(2.0)

    for _ in range(40):
        psm.set_jaw(0.02)
        time.sleep(0.05)

    print(f'Grasped {_get_parameter['target_block']}')

def lift_block(psm):

    print(f"Lifting {_get_parameter['target_block']}")

    move_grasped_object_to_pose(psm=psm,
                                grasped_object=_get_parameter['target_block'],
                                target_object=_get_parameter['target_block'],
                                rot_offset = Rotation.RPY(*_get_parameter['lift']['rot_offset']),
                                pos_offset = Vector(*_get_parameter['lift']['pos_offset']),
                                max_delta=_get_parameter['lift']['max_delta'], 
                                pos_deadband=_get_parameter['lift']['pos_deadband'], 
                                rot_deadband=_get_parameter['lift']['rot_deadband'])

    print(f"Lifted {_get_parameter['target_block']}")

    time.sleep(2.0)
    
def relocate_block(psm):

    print(f"Relocating {_get_parameter['target_block']} to {_get_parameter['target_peg']}")


    move_grasped_object_to_pose(psm=psm,
                                grasped_object=_get_parameter['target_block'],
                                target_object=_get_parameter['target_peg'],
                                rot_offset = Rotation.RPY(*_get_parameter['relocate']['rot_offset']),
                                pos_offset = Vector(*_get_parameter['relocate']['pos_offset']),
                                max_delta=_get_parameter['relocate']['max_delta'], 
                                pos_deadband=_get_parameter['relocate']['pos_deadband'], 
                                rot_deadband=_get_parameter['relocate']['rot_deadband'])

    print(f"Relocated {_get_parameter['target_block']} to {_get_parameter['target_peg']}")

    time.sleep(2.0)

    
def place_block(psm):

    print(f'Placing {_get_parameter['target_block']} on {_get_parameter['target_peg']}')

    move_grasped_object_to_pose(psm=psm,
                                grasped_object=_get_parameter['target_block'],
                                target_object=_get_parameter['target_peg'],
                                rot_offset = Rotation.RPY(*_get_parameter['place']['rot_offset']),
                                pos_offset = Vector(*_get_parameter['place']['pos_offset']),
                                max_delta=_get_parameter['place']['max_delta'], 
                                pos_deadband=_get_parameter['place']['pos_deadband'], 
                                rot_deadband=_get_parameter['place']['rot_deadband'])

    psm.set_jaw(0.08)

    print(f"Placed {_get_parameter['target_block']} on {_get_parameter['target_peg']}")

    time.sleep(2.0)
