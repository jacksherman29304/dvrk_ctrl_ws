# peg_task

Actual peg-transfer task scripts.

## Contents

peg_task/
├── config/
│   └── parameters.yaml
└── peg_task/
    ├── config.py          loads parameters.yaml, allows access to data and offsets etc.
    ├── ros_interface.py   ObjectPoseClient, SimControl
    ├── motion.py          psm_to_pose — the servo loop
    ├── routines.py        init_arm, pick_block, place_block
    ├── sequence.py        run_task — calls skills in order
    └── peg_transfer.py  main

## Used by
N/A