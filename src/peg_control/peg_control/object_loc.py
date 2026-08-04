import rclpy
from rclpy.node import Node

# block1/State message type: ambf_msgs/msg/RigidBodyState
from ambf_msgs.msg import RigidBodyState
from ambf_msgs.msg import ActuatorState

# import custom service 
from peg_interfaces.srv import GetObjectPose

class ObjectLocator(Node):

    def __init__(self):
        super().__init__('object_locator') # node name

        # subscriber to block1/State topic
        self.block1_sub = self.create_subscription(
            RigidBodyState,                         # message type
            '/ambf/env/phantom/block1/State',       # topic name
            self.block1_callback,                 # callback function
            10                                      # QoS queue depth
            )
        
        self.block2_sub = self.create_subscription(
            RigidBodyState,                         # message type
            '/ambf/env/phantom/block2/State',       # topic name
            self.block2_callback,                 # callback function
            10                                      # QoS queue depth
            )
        
        self.block3_sub = self.create_subscription(
            RigidBodyState,                         # message type
            '/ambf/env/phantom/block3/State',       # topic name
            self.block3_callback,                 # callback function
            10                                      # QoS queue depth
            )
        
        self.block4_sub = self.create_subscription(
            RigidBodyState,                         # message type
            '/ambf/env/phantom/block4/State',       # topic name
            self.block4_callback,                 # callback function
            10                                      # QoS queue depth
            )

                # subscriber to block1/State topic
        self.block5_sub = self.create_subscription(
            RigidBodyState,                         # message type
            '/ambf/env/phantom/block5/State',       # topic name
            self.block5_callback,                 # callback function
            10                                      # QoS queue depth
            )
                        # subscriber to block1/State topic
        self.block6_sub = self.create_subscription(
            RigidBodyState,                         # message type
            '/ambf/env/phantom/block6/State',       # topic name
            self.block6_callback,                 # callback function
            10                                      # QoS queue depth
            )

        self.peg4_sub = self.create_subscription(
            RigidBodyState,                         # message type
            '/ambf/env/phantom/peg4/State',       # topic name
            self.peg4_callback,                 # callback function
            10               
        )
               
        self.peg6_sub = self.create_subscription(
            RigidBodyState,                         # message type
            '/ambf/env/phantom/peg6/State',       # topic name
            self.peg6_callback,                 # callback function
            10               
        )

                
        self.peg7_sub = self.create_subscription(
            RigidBodyState,                         # message type
            '/ambf/env/phantom/peg7/State',       # topic name
            self.peg7_callback,                 # callback function
            10               
        )

        self.peg10_sub = self.create_subscription(
            RigidBodyState,                         # message type
            '/ambf/env/phantom/peg10/State',       # topic name
            self.peg10_callback,                 # callback function
            10               
        )

        self.peg13_sub = self.create_subscription(
            RigidBodyState,                         # message type
            '/ambf/env/phantom/peg13/State',       # topic name
            self.peg13_callback,                 # callback function
            10               
        )

        self.peg14_sub = self.create_subscription(
            RigidBodyState,                         # message type
            '/ambf/env/phantom/peg14/State',       # topic name
            self.peg14_callback,                 # callback function
            10               
        )

        self.psm1_sub = self.create_subscription(
            RigidBodyState,
            '/ambf/env/psm1/baselink/State',
            self.psm1_callback,
            10
        )

        self.psm2_sub = self.create_subscription(
            RigidBodyState,
            '/ambf/env/psm2/baselink/State',
            self.psm2_callback,
            10
        )

        self.cam_sub = self.create_subscription(
            RigidBodyState,
            '/ambf/env/phantom/CameraFrame/State',
            self.cam_callback,
            10
        )

        self.get_logger().info('Subscribed to /ambf/env/phantom/block1/State')

        self.object_pose = {}

        self.pose_service = self.create_service(
            GetObjectPose, # service type defined in peg_transfer_interfaces
            "get_object_pose", # service name
            self.get_object_pose_callback # callback function executed whenever service called

        )

    # callback function for block1 position
    def block1_callback(self, msg):
        self.object_pose['block1'] = msg.pose
        #self.get_logger().info(f'block1-state: {self.object_pose['block1']}')
        self.get_logger().info('block1 pose updated')

    def block2_callback(self, msg):
        self.object_pose['block2'] = msg.pose
        #self.get_logger().info(f'block2-state: {self.object_pose['block2']}')
        self.get_logger().info('block2 pose updated')

    def block3_callback(self, msg):
        self.object_pose['block3'] = msg.pose
        #self.get_logger().info(f'block3-state: {self.object_pose['block3']}')
        self.get_logger().info('block3 pose updated')

    def block4_callback(self, msg):
        self.object_pose['block4'] = msg.pose
        #self.get_logger().info(f'block4-state: {self.object_pose['block4']}')
        self.get_logger().info('block4 pose updated')

    def block5_callback(self, msg):
        self.object_pose['block5'] = msg.pose
        #self.get_logger().info(f'block5-state: {self.object_pose['block5']}')
        self.get_logger().info('block5 pose updated')

    def block6_callback(self, msg):
        self.object_pose['block6'] = msg.pose
        #self.get_logger().info(f'block6-state: {self.object_pose['block6']}')
        self.get_logger().info('block6 pose updated')

        
    def peg4_callback(self, msg):
        self.object_pose['peg4'] = msg.pose    
        #self.get_logger().info(f'peg4-pose: {self.object_pose['peg4']}')
        self.get_logger().info('peg4 pose updated')

    def peg6_callback(self, msg):
        self.object_pose['peg6'] = msg.pose    
        #self.get_logger().info(f'peg6-pose: {self.object_pose['peg6']}')
        self.get_logger().info('peg6 pose updated')  

    def peg7_callback(self, msg):
        self.object_pose['peg7'] = msg.pose    
        #self.get_logger().info(f'peg7-pose: {self.object_pose['peg7']}')
        self.get_logger().info('peg7 pose updated')     

    # callback function for peg10 position
    def peg10_callback(self, msg):
        self.object_pose['peg10'] = msg.pose    
        #self.get_logger().info(f'peg10-pose: {self.object_pose['peg10']}')
        self.get_logger().info('peg10 pose updated')

    def peg13_callback(self, msg):
        self.object_pose['peg13'] = msg.pose    
        #self.get_logger().info(f'peg13-pose: {self.object_pose['peg13']}')
        self.get_logger().info('peg13 pose updated')

    def peg14_callback(self, msg):
        self.object_pose['peg14'] = msg.pose    
        #self.get_logger().info(f'peg14-pose: {self.object_pose['peg14']}')
        self.get_logger().info('peg14 pose updated')

    # callback function for psm1 position
    def psm1_callback(self, msg):
        self.object_pose['psm1'] = msg.pose
        #self.get_logger().info(f'psm1-pose: {self.object_pose['psm1']}')
        self.get_logger().info('psm1 pose updated')

    # callback function for psm2 position
    def psm2_callback(self, msg):
        self.object_pose['psm2'] = msg.pose
        #self.get_logger().info(f'psm2-pose: {self.object_pose['psm2']}')
        self.get_logger().info('psm2 pose updated')
        
    # callback function for camera position
    def cam_callback(self, msg):
        self.object_pose['cam'] = msg.pose    
        #self.get_logger().info(f'cam-pose: {self.object_pose['cam']}')
        self.get_logger().info('camera pose updated')

    def get_object_pose(self, object_name:str):
        return self.object_pose[object_name]

    # service/cli approach
    def get_object_pose_callback(self, request, response):
        if request.object_name not in self.object_pose: # eventually change to object_states
            response.success = False
            return response
        
        # object_name is the string input defined in GetObjectPose.srv
        pose = self.object_pose[request.object_name]

        response.pose = pose # assign pose
        response.success = True # assign boolean as in GetObjectPose.srv structure

        return response # response sent to client via ROS2
        

# ROS2 entry point
def main(args=None):
    rclpy.init(args=args)
    
    # Runs init
    node = ObjectLocator()
 
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
