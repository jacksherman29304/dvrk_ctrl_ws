# da Vinci Research Kit (dVRK) Control Workspace
![ROS2](https://img.shields.io/badge/ROS2-Jazzy-blue)
![AMBF](https://img.shields.io/badge/AMBF-simulator-orange)
![Ubuntu](https://img.shields.io/badge/Ubuntu-24.04-E95420?logo=ubuntu&logoColor=white)
<!-- ![License](https://img.shields.io/badge/license-Apache_2.0-green) -->

ROS2 workspace for controlling the da Vinci Research Kit (dVRK).
This workspace is focused on the ICRA peg-transfer surgical robotics challenge, building upon their [challenge repository](https://github.com/surgical-robotics-ai/surgical_robotics_challenge/tree/icra2026-challenge).

## Requirements
- ROS2 Jazzy
- Ubuntu 24.04
- [AMBF Simulation Environment](https://github.com/WPI-AIM/ambf)

## Installation
```bash
git clone https://github.com/jacksherman29304/dvrk_ctrl_ws.git
cd dvrk_ctrl_ws
colcon build
source install/setup.bash


after initial installation, can just call:
cd dvrk_ctrl_ws
./rebuild.sh
this will automate above steps and execute launch file
```

## Status
Verified.
