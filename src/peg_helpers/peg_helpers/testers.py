class PSMTimeoutError(Exception):
    "Triggered when PSM motion fails and times out (>30s) - used for tracking test failure"
    pass 

def drop_detect(psm):
    if not psm.is_grasped(): # if drop detected
        return 1

    return 0