# RCLPY Imports
import rclpy
import threading
from rclpy.executors import MultiThreadedExecutor

# External Imports
import time

# Control Imports
from peg_control.tool_cmd import ToolCommand

# Task imports
from peg_task.config import load_config
from peg_task.ros_interface import ObjectPoseClient, SimControl
from peg_task.routines import PsmInit, init_handlers
from peg_task.routines import enter_scene, grasp_block, lift_block, relocate_block, place_block


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
    time.sleep(3.0)
    target_arm = psm2

    enter_scene(target_arm)
    grasp_block(target_arm) 
    lift_block(target_arm)
    relocate_block(target_arm)
    place_block(target_arm)

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
    