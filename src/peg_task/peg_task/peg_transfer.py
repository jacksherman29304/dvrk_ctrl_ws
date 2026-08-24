# RCLPY Imports
import rclpy
import threading
from rclpy.executors import MultiThreadedExecutor

# External Imports
import time
import random
import pandas as pd

# Helpers Imports
#from peg_helpers.randomise_env import randomise_env
from peg_helpers.testers import PSMTimeoutError, drop_detect

# Control Imports
from peg_control.tool_cmd import ToolCommand

# Task imports
from peg_task.config import load_config
from peg_task.ros_interface import ObjectPoseClient, SimControl
from peg_task.routines import PsmInit, init_handlers
from peg_task.routines import enter_scene, grasp_block, lift_block, relocate_block, place_block, block_passover, passover, reset_check


#------------------------- CLASS INSTANCES -------------------------#
rclpy.init()
object_pose_client = ObjectPoseClient() # Instance of service class
psm1 = ToolCommand('psm1')
psm2 = ToolCommand('psm2')
sim = SimControl()
init_handlers(object_pose_client) # pass client-side handler to routines,py


#------------------------- TASK PARAMETERS -------------------------#
pegs = ['peg4', 'peg6', 'peg10' , 'peg13', 'peg14'] # only peg topics available to ObjectLocate (not incliding peg7, which block5 sits on)
blocks = ['block2', 'block5'] # blocks used in simulation

#------------------------- RUN TASK LOOP -------------------------#  
def run_task(parameters):
    params = parameters # parameters.yaml - offsets, objects etc.
    
    df = pd.DataFrame(columns=['iteration', 'pass_fail', 'failure_stage', 'time', 'drops', 'distance_psm1', 'distance_psm2', 'total_distance', 'block2_target_peg', 'block5_target_peg'])
 
    pass_fail_log = []
    failure_stage_log = []
    time_log = []
    filtered_time_log = []
    drops_log = []
    distance_psm1_log = []
    distance_psm2_log = []
    total_distance_log = []
    block2_target_peg_log = []
    block5_target_peg_log = []

    TEST_NO = 1
    TEST_CONFIG_FILE = '/home/dvrk-team/dvrk_ctrl_ws/src/peg_sim/ADF/Phantoms/Pegboards/test_1.yaml' # change this to adapt expected block position checks
    RESULTS_OUTPUT_PATH = (f'/home/dvrk-team/Desktop/test{TEST_NO}_results.csv') # REMEMBER to change launch.yaml
    
    LOOPS = 40
    SEED = 32



    random.seed(SEED)
    for i in range(LOOPS):
        print(f"ITERATION {i}")
        # Init test vars
        drop_count = 0
        distance_psm1 = 0.0
        distance_psm2 = 0.0


        # reset simulation environment (e.g. blocks, PSMs)
        sim.reset_env() 
        time.sleep(3.0)

        # checks if sim has actually reset (prevents cascading failures)
        if not reset_check(path=TEST_CONFIG_FILE):

            pass_fail_log.append('INVALID')
            failure_stage_log.append('INVALID')
            time_log.append('INVALID')
            drops_log.append('INVALID')
            distance_psm1_log.append('INVALID')
            distance_psm2_log.append('INVALID')
            total_distance_log.append('INVALID')
            block2_target_peg_log.append('INVALID')
            block5_target_peg_log.append('INVALID')

            sim.reset_bodies()
            sim.reset_env()
            time.sleep(2.0)

            continue

        # randomly select two pegs to allocate to blocks
        peg = random.sample(pegs, k=2)

        # start timer
        t0 = time.perf_counter()

        try: 
            PsmInit(psm=psm2, jp_init=params['init']['psm2_init'], jaw_init=params['init']['jaw_open'], max_wait=10, reference_block='block5')
            PsmInit(psm=psm1, jp_init=params['init']['psm1_init'], jaw_init=params['init']['jaw_open'], max_wait=10, reference_block='block2')
            time.sleep(2.0)

            # Block 5 peg transfer
            distance_psm2 += enter_scene(psm2, 'block5')
            distance_psm2 += grasp_block(psm2, 'block5') 
            drop_count += drop_detect(psm2) 
            distance_psm2 += lift_block(psm2, 'block5')
            drop_count += drop_detect(psm2)
            grasp_distance, passover_distance = passover(grasp_psm=psm2, passover_psm=psm1, target_block='block5')
            distance_psm2+=grasp_distance
            distance_psm1+=passover_distance
            psm2.set_jaw(0.08)
            drop_count += drop_detect(psm1)
            PsmInit(psm=psm2, jp_init=params['init']['psm2_init'], jaw_init=params['init']['jaw_open'], max_wait=10)
            relocate_block(psm1, 'block5', peg[0])
            drop_count += drop_detect(psm1)
            distance_psm1 += place_block(psm1, 'block5', peg[0]) 

            # Reset PSMs
            PsmInit(psm=psm2, jp_init=params['init']['psm2_init'], jaw_init=params['init']['jaw_open'], max_wait=10)
            PsmInit(psm=psm1, jp_init=params['init']['psm1_init'], jaw_init=params['init']['jaw_open'], max_wait=10)
            time.sleep(2.0)

            # Block 2 peg transfer
            distance_psm1 += enter_scene(psm1, 'block2')
            distance_psm1 += grasp_block(psm1, 'block2')
            drop_count += drop_detect(psm1)
            distance_psm1 += lift_block(psm1, 'block2')
            drop_count += drop_detect(psm1)
            grasp_distance, passover_distance = passover(grasp_psm=psm1, passover_psm=psm2, target_block='block2')
            distance_psm1+=grasp_distance
            distance_psm2+=passover_distance
            psm1.set_jaw(0.08)
            drop_count += drop_detect(psm2)
            PsmInit(psm=psm1, jp_init=params['init']['psm1_init'], jaw_init=params['init']['jaw_open'], max_wait=10)
            distance_psm2+=relocate_block(psm2, 'block2', peg[1])
            drop_count += drop_detect(psm2)
            distance_psm2+=place_block(psm2, 'block2', peg[1])

            # Reset PSMs
            PsmInit(psm=psm2, jp_init=params['init']['psm2_init'], jaw_init=params['init']['jaw_open'], max_wait=10)
            PsmInit(psm=psm1, jp_init=params['init']['psm1_init'], jaw_init=params['init']['jaw_open'], max_wait=10)
            
            # time processing
            elapsed= round(time.perf_counter()-t0, 2)
            time_log.append(elapsed)

            # Append data logs
            pass_fail_log.append("PASS")
            failure_stage_log.append("N/A")
            drops_log.append(drop_count) 
            distance_psm1_log.append(distance_psm1)
            distance_psm2_log.append(distance_psm2)
            total_distance_log.append(distance_psm1+distance_psm2)
            block2_target_peg_log.append(peg[1])
            block5_target_peg_log.append(peg[0])

        except PSMTimeoutError as e: #exception called if timeout occurs in psm_to_pose, 'e' is the exception object and returns error string
            elapsed= round(time.perf_counter()-t0, 2)
            print(f"ITERATION {i} FAILED")
            pass_fail_log.append("FAIL")
            failure_stage_log.append(e.get_failure_stage())
            time_log.append(elapsed)
            drops_log.append(drop_count)
            distance_psm1_log.append(distance_psm1)
            distance_psm2_log.append(distance_psm2)
            total_distance_log.append(distance_psm1 + distance_psm2)
            block2_target_peg_log.append(peg[1])
            block5_target_peg_log.append(peg[0])


    # filter out 'FAIL' string data - only looking for integers and floats    
    filtered_time_log = list(filter(lambda i: isinstance(i, (int, float)), time_log))

    if len(filtered_time_log) == 0:
        print("No succesful peg transfers - no data available")
    elif len(filtered_time_log) == 1:
        measured_time = filtered_time_log[0]
        minutes = int(measured_time // 60)
        seconds = measured_time % 60
        print(f"Execution time: {minutes}m {seconds}s")
    else:
        average_time = round(sum(filtered_time_log) / len(filtered_time_log), 2)
        minutes = int(average_time // 60)
        seconds = average_time % 60
        print(f"Average Execution time over {LOOPS} iterations: {minutes}m {seconds}s")


    df['iteration'] = range(LOOPS)
    df['pass_fail'] = pass_fail_log
    df['failure_stage'] = failure_stage_log
    df['time'] = time_log
    df['drops'] = drops_log
    df['distance_psm1'] = distance_psm1_log
    df['distance_psm2'] = distance_psm2_log
    df['total_distance'] = total_distance_log
    df['block2_target_peg'] = block2_target_peg_log
    df['block5_target_peg'] = block5_target_peg_log
 
    print(df)
    df.to_csv(RESULTS_OUTPUT_PATH, index=False)

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
    