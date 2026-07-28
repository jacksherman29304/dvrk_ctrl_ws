# peg_bringup

Contains laubch files and associated checks to ensure smooth interactions between AMBF And CRTK topics.

## Contents
'system_launch.py' - launch file that successively launches AMBF, CRTK, and all remaining peg_control nodes
'ambf_live.py' - subscribes to ambf topics and reports whether topics are live or not - impacts launch file sequence
'crtk_live.py' - subscribes to CRTK topics and reports whether topics are live or not - impacts launch file sequence

## Used by
N/A