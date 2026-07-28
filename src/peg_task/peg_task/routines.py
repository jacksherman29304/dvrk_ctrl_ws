# psm init, locate block etc.
 
import time
import numpy as np
from peg_math.conversions import ps_to_frame


#------------------------- PSM INIT -------------------------#
# # Check CRTK BASED CONTROL SCRIPT AND ALSO ORIGINAL PEG TRANSFER
def PsmInit(psm, jp_init, jaw_init, max_wait):

    psm.move_jp(jp_init)
    psm.set_jaw(jaw_init)

    # Timer added to allow PSMs to reach initialised joint positions before measuring frames - prevents inaccurate early readings
    start = time.time() # starts timer for elapsed time
    while time.time() - start < max_wait: # whilst under max wait time in seconds

        js = psm.measured_js # measure current joint state of psm

        # current_jp becomes measured joint state if measured js is not empty and has at least 1 value
        current_jp = js.position if js is not None and len(js.position) > 0 else None 

        # if updated current_jp has read valid data and this joint position is within 0.005 tolerance of target joint position, break loop and enable frame readings
        if current_jp is not None and np.allclose(current_jp, jp_init, atol=0.005):
            break
        time.sleep(0.002)
    else: # error detection
        print(f"WARNING: {psm} did not converge to init position within {max_wait}s timeout")

    T_base_w = ps_to_frame(psm.T_b_w) # Grab base in world pose from psm2/T_b_w and convert to frame
    T_ee_base = ps_to_frame(psm.measured_cp) # Grab ee relative to base pose from psm2/measured_cp and convert to frame
    T_ee_w = T_base_w * T_ee_base # ee in world is multiplication of previous transforms

    return T_base_w, T_ee_base, T_ee_w