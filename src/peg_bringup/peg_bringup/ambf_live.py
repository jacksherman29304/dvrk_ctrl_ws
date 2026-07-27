import rclpy
from rclpy.node import Node
from ambf_msgs.msg import RigidBodyState
import sys



class AmbfLive(Node):
    def __init__(self):
        super().__init__('ambf_live')

        # AMBF topic names
        namespace = "/ambf/env/"
        psm1 = 'psm1'
        psm2 = 'psm2'
        camera = 'phantom'


        self.psm1_baselink_topic = namespace + psm1 + '/baselink/State' # [ambf_msgs/msg/RigidBodyState]
        self.psm2_baselink_topic = namespace + psm2 + '/baselink/State' # [ambf_msgs/msg/RigidBodyState]

        self.camera_topic = namespace + camera + '/CameraFrame/State' # [ambf_msgs/msg/RigidBodyState]

        # subscribers - baselinks for both PSMs
        self.psm1_baselink_sub = self.create_subscription(RigidBodyState, self.psm1_baselink_topic,  self.psm1_baselink_cb, 1)
        self.psm2_baselink_sub = self.create_subscription(RigidBodyState, self.psm2_baselink_topic,  self.psm2_baselink_cb, 1)

        # subscriber - camera positon
        self.camera_sub = self.create_subscription(RigidBodyState, self.camera_topic,  self.camera_cb, 1)


        # Storage Variables - might be unnecessary
        self.psm1_baselink = RigidBodyState()
        self.psm2_baselink = RigidBodyState()
        self.camera = RigidBodyState()
    

        # Flags
        self.psm1_baselink_flag = False
        self.psm2_baselink_flag = False
        self.camera_flag = False


        # Flag that spin_until_future_complete watches
        self.ready_future = rclpy.task.Future()

    # Checks if all topics have been successfully subscribed to and reading values, sets future value to True if satisfied
    # private function
    def _check_all_topics_live(self):
        if(self.psm1_baselink_flag and self.psm2_baselink_flag and self.camera_flag ):
            if not self.ready_future.done():
                self.ready_future.set_result(True)


    def psm1_baselink_cb(self, msg):
        self.psm1_baselink = msg
        self.psm1_baselink_flag = True
        self._check_all_topics_live()

    def psm2_baselink_cb(self, msg):
        self.psm2_baselink = msg
        self.psm2_baselink_flag = True
        self._check_all_topics_live()

    def camera_cb(self, msg):
        self.camera = msg
        self.camera_flag = True
        self._check_all_topics_live()

def main():
    rclpy.init()
    node = AmbfLive() # Create instance of node
    rclpy.spin_until_future_complete(node, node.ready_future, timeout_sec=20.0) # spins AmbfLive node until node.ready_future is True (all topics subscribed to and reading values) - times out after 20 seconds of waiting

    if node.ready_future.done(): # if True, print to terminal, exit_code = 0 = success
        node.get_logger().info('All AMBF topics live')
        exit_code = 0
    else: # if False until timeout, print error to terminal, exit_code = 1 = failure
        node.get_logger().error('Timed out waiting for AMBF topics')
        exit_code = 1


    node.destroy_node()
    rclpy.shutdown()
    sys.exit(exit_code) # Event handler in launch file to inspect this value

if __name__ == '__main__':
    main()