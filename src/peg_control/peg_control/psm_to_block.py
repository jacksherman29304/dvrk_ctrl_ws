import rclpy
from rclpy.node import Node

from utilities.psm1_cmd import Psm1Command
from utilities.psm2_cmd import Psm2Command
from utilities.object_loc import ObjectLocator
from peg_math.conversions import rbs_to_frame




class psm_to_block(Node):
    def __init__(self, psm: str):
        super().__init__(f'{psm}_to_block')
        
        self.psm = psm # selected psm arm
        self.object_loc = ObjectLocator() # ObjectLocator instance

        self.timer = self.create_timer(0.1, self.control_loop)  # e.g. 10 Hz

        if self.psm == 'psm1':
            self.psm_cmd = Psm1Command()
        else:
            self.psm_cmd = Psm2Command()

    def control_loop(self):
        block1_rbs = self.object_loc.get_object_pose('block1') # RigidBodyState of Block1
        block1_pose = rbs_to_frame(block1_rbs)
        self.psm_cmd.servo_cp(block1_pose)



# ROS2 entry point
def main(args=None):
    rclpy.init(args=args)

    # tool_to_block node
    node = psm_to_block('psm1')
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

        