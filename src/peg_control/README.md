# peg_control

Scripts to control and monitor position and actions of simulation objects.

## Contents
'object_loc.py' - subscribes to simulation object poses whilst behaving as a service to peg task files, which request current object positons - eventually to be replaced by camera perception
'tool_cmd.py' - used to monitor and command PSMs via a range of CRTK topics

## Redundant files
'psm1_cmd.py' - combined with psm2_cmd.py to produce tool_cmd.py
'psm2_cmd.py' - combined with psm1_cmd.py to produce tool_cmd.py
'psm_to_block' - early development peg transfer task file

## Used by
peg_task