# RCLPY Imports
import rclpy
import threading
from rclpy.executors import MultiThreadedExecutor

# External Imports
import time

# Math Imports
from peg_math import randomise_env

# Control Imports
from peg_control.tool_cmd import ToolCommand

# Task imports
from peg_task.config import load_config
from peg_task.ros_interface import ObjectPoseClient, SimControl
from peg_task.routines import PsmInit, init_handlers
from peg_task.routines import enter_scene, grasp_block, lift_block, relocate_block, place_block, block_passover


#------------------------- CLASS INSTANCES -------------------------#
rclpy.init()
object_pose_client = ObjectPoseClient() # Instance of service class
psm1 = ToolCommand('psm1')
psm2 = ToolCommand('psm2')
sim = SimControl()
init_handlers(object_pose_client) # pass client-side handler to routines,py

#------------------------- RUN TASK LOOP -------------------------#  
def run_task(parameters):
    params = parameters # parameters.yaml - offsets, objects etc.
    sim.reset_env() # Reset all simulation bodies (e.g. blocks, PSMs)
    time.sleep(2.0)
    PsmInit(psm=psm2, jp_init=params['init']['psm2_init'], jaw_init=params['init']['jaw_open'], max_wait=10)
    PsmInit(psm=psm1, jp_init=params['init']['psm1_init'], jaw_init=params['init']['jaw_open'], max_wait=10)
    time.sleep(3.0)

    # lift block 5 and reloate
    enter_scene(psm2, 'block5')
    grasp_block(psm2, 'block5') 
    lift_block(psm2, 'block5')
    block_passover(psm1, 'block5')
    psm2.set_jaw(0.08)
    relocate_block(psm1, 'block5', 'peg10')
    place_block(psm1, 'block5', 'peg10')

    # lift block 2 and relocate
    # current issue lies with hard offets not applying to all blocks in all positions
    PsmInit(psm=psm2, jp_init=params['init']['psm2_init'], jaw_init=params['init']['jaw_open'], max_wait=10)
    PsmInit(psm=psm1, jp_init=params['init']['psm1_init'], jaw_init=params['init']['jaw_open'], max_wait=10)
    time.sleep(2.0)
    enter_scene(psm1, 'block2')
    grasp_block(psm1, 'block2') 
    lift_block(psm1, 'block2')
    block_passover(psm2, 'block2')
    psm1.set_jaw(0.08)
    relocate_block(psm2, 'block2', 'peg7')
    place_block(psm2, 'block2', 'peg7')
    

    
    # psm1.set_jaw(0.08)
    # relocate_block(psm1, 'block5', 'peg10')
    # place_block(psm1, 'block5', 'peg10')

def main():
    # input_path = '/home/dvrk-team/dvrk_ctrl_ws/src/peg_sim/ADF/Phantoms/Pegboards/pegboard_asymmetric.yaml'
    # output_path = '/home/dvrk-team/dvrk_ctrl_ws/src/peg_sim/ADF/Phantoms/Pegboards/pegboard_asymmetric_out.yaml'
    # randomise_env(input_path, output_path)
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
    