~/dvrk_ctrl_ws

rm -rf build install log

colcon build

source install/setup.bash

ros2 launch peg_bringup system_launch.py
