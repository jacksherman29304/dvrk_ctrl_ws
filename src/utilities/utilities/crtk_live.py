import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
import sys



class CrtkLive(Node):
    def __init__(self):
        super().__init__('crtk_live')

        # CRTK topic names
        namespace = "/CRTK/"
        psm1 = 'psm1'
        psm2 = 'psm2'

        self.psm1_Tbw_topic = namespace + psm1 + '/T_b_w' # [geometry_msgs/msg/PoseStamped] 
        self.psm2_Tbw_topic = namespace + psm2 + '/T_b_w' # [geometry_msgs/msg/PoseStamped] 

        self.psm1_measured_cp_topic = namespace + psm1 + '/measured_cp' # [geometry_msgs/msg/PoseStamped] 
        self.psm2_measured_cp_topic = namespace + psm2 + '/measured_cp' # [geometry_msgs/msg/PoseStamped] 


        # subscribers - T_b_w for both PSMs
        self.psm1_Tbw_sub = self.create_subscription(PoseStamped, self.psm1_Tbw_topic,  self.psm1_Tbw_cb, 1)
        self.psm2_Tbw_sub = self.create_subscription(PoseStamped, self.psm2_Tbw_topic, self.psm2_Tbw_cb, 1)

        # subscribers - measured_cp for both PSMs
        self.psm1_measured_cp_sub = self.create_subscription(PoseStamped, self.psm1_measured_cp_topic, self.psm1_measured_cp_cb, 1)
        self.psm2_measured_cp_sub = self.create_subscription(PoseStamped, self.psm2_measured_cp_topic, self.psm2_measured_cp_cb, 1)

        # Storage Variables - might be unnecessary
        self.psm1_Tbw = PoseStamped()
        self.psm2_Tbw = PoseStamped()
        self.psm1_measured_cp = PoseStamped()
        self.psm2_measured_cp = PoseStamped()

        # Flags
        self.psm1_Tbw_flag = False
        self.psm2_Tbw_flag = False
        self.psm1_measured_cp_flag = False
        self.psm2_measured_cp_flag = False


        # Flag that spin_until_future_complete watches
        self.ready_future = rclpy.task.Future()

    # Checks if all topics have been successfully subscribed to and reading values, sets future value to True if satisfied
    # private function
    def _check_all_topics_live(self):
        if(self.psm1_Tbw_flag and self.psm2_Tbw_flag and self.psm1_measured_cp_flag and self.psm2_measured_cp_flag):
            if not self.ready_future.done():
                self.ready_future.set_result(True)
        
    def psm1_Tbw_cb(self, msg):
        self.psm1_Tbw = msg
        self.psm1_Tbw_flag = True
        self._check_all_topics_live() # called in each as don't know which topic will be last

    def psm2_Tbw_cb(self, msg):
        self.psm2_Tbw = msg
        self.psm2_Tbw_flag = True
        self._check_all_topics_live()

    def psm1_measured_cp_cb(self, msg):
        self.psm1_measured_cp = msg
        self.psm1_measured_cp_flag = True
        self._check_all_topics_live()

    def psm2_measured_cp_cb(self, msg):
        self.psm2_measured_cp = msg
        self.psm2_measured_cp_flag = True
        self._check_all_topics_live()

def main():
    rclpy.init()
    node = CrtkLive() # Create instance of node
    rclpy.spin_until_future_complete(node, node.ready_future, timeout_sec=20.0) # spins CrtkLive node until node.ready_future is True (all topics subscribed to and reading values) - times out after 20 seconds of waiting

    if node.ready_future.done(): # if True, print to terminal, exit_code = 0 = success
        node.get_logger().info('All CRTK topics live')
        exit_code = 0
    else: # if False until timeout, print error to terminal, exit_code = 1 = failure
        node.get_logger().error('Timed out waiting for CRTK topics')
        exit_code = 1


    node.destroy_node()
    rclpy.shutdown()
    sys.exit(exit_code) # Event handler in launch file to inspect this value

if __name__ == '__main__':
    main()