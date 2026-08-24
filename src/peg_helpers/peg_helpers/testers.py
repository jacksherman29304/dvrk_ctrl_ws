class PSMTimeoutError(Exception):
    # Triggered when PSM motion fails and times out (>30s) - used for tracking test failure"
    # Failure stage passed as input for monitoring
    def __init__(self, failure_stage:str):

        self.failure_stage = failure_stage

    def get_failure_stage(self):
        return self.failure_stage


# checks is_grasped boolean to detect block drops
def drop_detect(psm):
    if not psm.is_grasped(): # if drop detected
        return 1

    return 0