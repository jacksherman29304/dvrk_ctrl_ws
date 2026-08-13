from rclpy.node import Node
from std_msgs.msg import Empty
from peg_interfaces.srv import GetObjectPose # sourcing ros workspaces will service file path apparent
import time

# ------------------------- OBJECT POSITION CLIENT NODE CLASS -------------------------#   
class ObjectPoseClient(Node):

    def __init__(self):
        super().__init__('object_pose_client') # Node name
        self.cli = self.create_client(GetObjectPose, '/get_object_pose')

    def wait_for_server(self, timeout=10.0):
        if not self.cli.wait_for_service(timeout_sec=timeout):
            raise RuntimeError(
                f'/get_object_pose unavailable after {timeout}s — is object_loc running?'
            )

        self.req = GetObjectPose.Request()

    def get_object_pose(self, object_name:str):

        request = GetObjectPose.Request()
        request.object_name = object_name
        
        future = self.cli.call_async(request)
        #rclpy.spin_until_future_complete(self, future)
        while not future.done():
            time.sleep(0.01)

        return future.result()
    

#------------------------- AMBF SIM CONTROL  -------------------------#  

class SimControl(Node):

    def __init__(self):
        super().__init__('sim_controller') # Node name
        self.reset_bodies_cmd = self.create_publisher(Empty ,'/ambf/env/World/Command/Reset/Bodies', 1)
        self.reset_world_cmd = self.create_publisher(Empty, '/ambf/env/World/Command/Reset', 1)

    def reset_bodies(self): # Reset environment bodies
        self.reset_bodies_cmd.publish(Empty())

    def reset_env(self):
        self.reset_world_cmd.publish(Empty())
