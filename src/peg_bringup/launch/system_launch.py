from launch import LaunchDescription
from launch.actions import ExecuteProcess, RegisterEventHandler, LogInfo, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.event_handlers import OnProcessExit
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():

    sim_share = get_package_share_directory('peg_sim') # get ADF, ambf_shaders, launch.yaml from peg_sim share directory

    ambf_arg = DeclareLaunchArgument(
        'scene_indices',
        default_value= '15,16,2,3,4,5',
        description='AMBF multibody indices. '
                    'asymmetric pegboard = 15,16,2,3,4,5   '
                    'symmetric with wall = 14,16,2,3,4,5',        

    )

    
    # Launch ambf simulation
    ambf_launch = ExecuteProcess(
        cmd=[
            'ambf_simulator',
            '--launch_file', 'launch.yaml',
            '-l', LaunchConfiguration('scene_indices'),
            '-p', '200', '-t1',
            '--override_max_comm_freq', '100',
            '--override_min_comm_freq', '100',
        ],
        cwd=sim_share, # points to share directory so configs can be found
        output='screen',

        # cmd=[
        #     '/home/dvrk-team/internship/peg_transfer/run_env_pegboard_asymmetric.sh'
        # ],
        # cwd = '/home/dvrk-team/internship/peg_transfer',
        # shell = True,
        # output = 'screen'
    )

    # Checking whether AMBF topics are live
    ambf_live = Node(
        package = 'peg_bringup',
        executable = 'ambf_live',
        name = 'ambf_live',
        output = 'screen'  
    )

    # Launch CRTK interface
    crtk_launch = ExecuteProcess(
        cmd=[
            'python3',
            '/home/dvrk-team/internship/peg_transfer/scripts/launch_crtk_interface.py',

        ],
        cwd = '/home/dvrk-team/internship/peg_transfer',
          env={
                    **os.environ,
                    "PYTHONPATH": os.pathsep.join([
                        "/home/dvrk-team/internship/peg_transfer/scripts",
                        os.environ.get("PYTHONPATH", "")
                    ])
                },
        output = 'screen'

    )

    # Checking whether CRTK topics are live
    crtk_live = Node(
        package = 'peg_bringup',
        executable = 'crtk_live',
        name = 'crtk_live',
        output = 'screen'  
    )

    # Launch obj_loc node
    object_locate_launch = Node(
        package = 'peg_control',
        executable = 'object_loc',
        name = 'object_loc',
        output = 'screen'  
        )

    # camera_interface_launch = Node(
    #     package = 'peg_perception',
    #     executable = 'camera_interface',
    #     name = 'camera_interface',
    #     output = 'screen'
    # )
    
    # psm1_command_launch = Node(
    #     package = 'peg_control',
    #     executable = 'psm1_cmd',
    #     name = 'psm1_cmd',
    #     output = 'screen'  

    # )

    # psm2_command_launch = Node(
    #     package = 'peg_control',
    #     executable = 'psm2_cmd',
    #     name = 'psm2_cmd',
    #     output = 'screen'  

    # )

    # 'context' doesnt do anything, this is just the ros2 launch function required syntax
    # event contains details for ambf_live (the target action)
    def on_ambf_live_exit(event, context):
        if event.returncode == 0: # inspect ambf_live return code, if success, launch crtk (launch crtk, crtk_live etc.)
            return[
                LogInfo(msg='AMBF topics confirmed live — starting crtk.'),
                crtk_launch, # launch CRTK
                crtk_live, # check CRTK topics live
                crtk_handler # respond to status of topics
            ]
        else:
            return[
                LogInfo(msg=f'ambf_live exited with code {event.returncode} - crtk not started'),
            ]

    # 'context' doesnt do anything, this is just the ros2 launch function required syntax
    # event contains details for crtk_live (the target action)
    def on_crtk_live_exit(event, context):
        if event.returncode == 0: # inspect crtk_live return code, if success, launch remaining nodes (object-locate, psm-cmd etc.)
            return[
                LogInfo(msg='CRTK topics confirmed live — starting remaining nodes.'),
                object_locate_launch,
                # psm1_command_launch,
                # psm2_command_launch
            ]
        else:
            return[
                LogInfo(msg=f'crtk_live exited with code {event.returncode} - remaining nodes not started'),
            ]

    ambf_handler = RegisterEventHandler(
        OnProcessExit(
            target_action=ambf_live,
            on_exit= on_ambf_live_exit # once ambf_live exits, executre this callback function
        )
    )

    crtk_handler = RegisterEventHandler(
        OnProcessExit(
            target_action=crtk_live,
            on_exit= on_crtk_live_exit # once crtk_live exits, executre this callback function
        )
    )



    return LaunchDescription([
        ambf_arg,
        ambf_launch, # launch ambf
        ambf_live, # check topics are live
        ambf_handler # respond to status of topics
        # camera_interface_launch
    ])