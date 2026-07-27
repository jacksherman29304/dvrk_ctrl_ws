import rclpy
from rclpy.node import Node


#Type: geometry_msgs/
from geometry_msgs.msg import PoseStamped
#Imports ROS messages for joint state (position (rad or m), velocity (rad/s or m/s), effort (Nm or N)) - joint
#Type: sensor_msgs/msg/
from sensor_msgs.msg import JointState
#Rotation class used to represent and convert 3D rotation in various formats (e.g., rotation matrix, quaternion, Euler angles)
from PyKDL import Vector, Rotation, Frame

class Psm2Command(Node):
    def __init__(self):
        super().__init__('psm2_command')

        # CRTK topic names
        namespace = "/CRTK/"
        self.tool = 'psm2'
        self.measured_js_topic = namespace + self.tool + "/measured_js"
        self.measured_cp_topic = namespace + self.tool + "/measured_cp"
        self.servo_jp_topic = namespace + self.tool + "/servo_jp"
        self.servo_cp_topic = namespace + self.tool + "/servo_cp"
        self.base_world_topic = namespace + self.tool + "/T_b_w"
        self.jaw_angle_topic = namespace + self.tool +"/jaw/servo_jp"

        self.move_cp_topic = namespace + self.tool + "/move_cp" # Move PSM until end-effector (relative to base) is in new position (relative to base)
        self.move_cp_pub = self.create_publisher(PoseStamped, self.move_cp_topic, 1) # Publisher to /move_cp topic

        self.move_jp_topic = namespace + self.tool + "/move_jp"  # Move PSM joint position (relative to base) using custom joint-array
        self.move_jp_pub = self.create_publisher(JointState, self.move_jp_topic, 1) # Publisher to /move_jp topic

        self.measured_js = JointState() # JoinState is topic type
        self.measured_cp = PoseStamped() # PoseStamped is topic type

        self.servo_jp_msg = JointState()
        self.servo_cp_msg = PoseStamped()

        self.T_b_w = PoseStamped()

        # subscribers - read position data from respective topic, triggering associated function
        self.measured_js_sub = self.create_subscription(JointState, self.measured_js_topic, self.measured_js_cb, 1)
        self.measured_cp_sub = self.create_subscription(PoseStamped, self.measured_cp_topic, self.measured_cp_cb, 1)
        # subscribe to base in world position for an inputted psm
        self.b_w_sub = self.create_subscription(PoseStamped, self.base_world_topic, self.b_w_cb, 1)

        # publishers - publish position data to respective topic
        self.servo_jp_pub = self.create_publisher(JointState, self.servo_jp_topic, 1)
        self.servo_cp_pub  = self.create_publisher(PoseStamped, self.servo_cp_topic, 1)
        self.servo_jaw_angle_pub = self.create_publisher(JointState, self.jaw_angle_topic, 1)

    def measured_js_cb(self, msg):
        self.measured_js = msg

    def measured_cp_cb(self, msg):
        self.measured_cp = msg

    def servo_cp(self, frame: Frame):
        msg = PoseStamped()

        pos = frame.p # extract frame position vector
        rot = frame.M # extract frame rotation

        qx, qy, qz, qw = rot.GetQuaternion()

        # Update position
        msg.pose.position.x = pos.x()
        msg.pose.position.y = pos.y()
        msg.pose.position.z = pos.z()

        # Update orientation
        msg.pose.orientation.x = float(qx)
        msg.pose.orientation.y = float(qy)
        msg.pose.orientation.z = float(qz)
        msg.pose.orientation.w = float(qw)
        
        self.servo_cp_pub.publish(msg) # publish Pose to cp topic

        # Accepts Frame, converts it to PoseStamped, publishes to /move_cp topic
    def move_cp(self, frame: Frame):
        msg = PoseStamped()

        pos = frame.p # extract frame position vector
        rot = frame.M # extract frame rotation

        qx, qy, qz, qw = rot.GetQuaternion()

        # Update position
        msg.pose.position.x = pos.x()
        msg.pose.position.y = pos.y()
        msg.pose.position.z = pos.z()

        # Update orientation
        msg.pose.orientation.x = float(qx)
        msg.pose.orientation.y = float(qy)
        msg.pose.orientation.z = float(qz)
        msg.pose.orientation.w = float(qw)
        
        self.move_cp_pub.publish(msg) # publish Pose to move_cp topic  

    # Accepts array, converts it to JointState, publishes to /move_jp topic
    def move_jp(self, array):
        msg = JointState()
        msg.position = list(array) # publish 6 DOF joint array
        self.move_jp_pub.publish(msg) 

    def servo_jp(self, joint_positions: list):
        msg = JointState()

        msg.position = list(joint_positions)

        self.servo_jp_pub.publish(msg)

    # subscribe to psm base-in-world topic, accepts it as a posestamped
    # convert to frame

    def b_w_cb(self, msg):
        self.T_b_w = msg # update base in world state
        
    
    # publish to /CRTK/psm1/jaw/servo_jp with commanded jaw width [0] - just want the x value
    def set_jaw(self, jaw_angle: float):
        msg = JointState()

        msg.position = [jaw_angle] # applying single value
        self.servo_jaw_angle_pub.publish(msg)
    
# ####### This only works if it is a separate package as the full script is ran - so has no impact this way
# # ROS2 entry point
def main(args=None):
    rclpy.init(args=args)
    
    # Runs init
    node = Psm2Command()
 
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
