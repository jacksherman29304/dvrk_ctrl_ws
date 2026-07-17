from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():
    
    # Launch ambf simulation
    ambf_launch = ExecuteProcess(
        cmd=[
            '/home/dvrk-team/internship/peg_transfer/run_env_pegboard_asymmetric.sh'
        ],
        cwd = '/home/dvrk-team/internship/peg_transfer',
        shell = True,
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

    # Launch obj_loc node
    object_locate_launch = Node(
        package = 'utilities',
        executable = 'object_loc',
        name = 'object_loc',
        output = 'screen'  
        )
    
    psm1_command_launch = Node(
        package = 'utilities',
        executable = 'psm1_cmd',
        name = 'psm1_cmd',
        output = 'screen'  

    )

    psm2_command_launch = Node(
        package = 'utilities',
        executable = 'psm2_cmd',
        name = 'psm2_cmd',
        output = 'screen'  

    )


    return LaunchDescription([
        ambf_launch,
        crtk_launch,
        object_locate_launch,
        psm1_command_launch,
        psm2_command_launch

    ])