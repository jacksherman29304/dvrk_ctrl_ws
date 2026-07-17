import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/dvrk-team/dvrk_ctrl_ws/install/peg_control'
