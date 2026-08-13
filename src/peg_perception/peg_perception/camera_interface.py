import rclpy
from rclpy.node import Node

# Type: sensor_msgs/msg/
from sensor_msgs.msg import CameraInfo, Image, PointCloud2

#Rotation class used to represent and convert 3D rotation in various formats (e.g., rotation matrix, quaternion, Euler angles)
from PyKDL import Vector, Rotation, Frame
import numpy as np
from sensor_msgs_py import point_cloud2

# CV bridge is a ROS package that provides an interface between ROS and OpenCV, allowing for easy conversion between ROS image messages and OpenCV image formats.
from cv_bridge import CvBridge

class CameraInterface(Node):
    def __init__(self):
        super().__init__('CameraInterface')
        self.cv_bridge = CvBridge() #  Instance of the CvBridge class
        self.l_count = [0]
        self.r_count = [0]

        self.left_camera_info_topic = '/ambf/env/stereo/left/CameraInfo'
        self.right_camera_info_topic = '/ambf/env/stereo/right/CameraInfo'

        self.left_camera_image_topic = '/ambf/env/stereo/left/ImageData'
        self.right_camera_image_topic = '/ambf/env/stereo/right/ImageData'

        self.left_camera_depth_topic = '/ambf/env/stereo/left/DepthData'
        self.right_camera_depth_topic = '/ambf/env/stereo/right/DepthData'  

        # subscribes to CameraInfo ROS topics for left and right stereo cameras
        self.left_info_sub = self.create_subscription(CameraInfo, self.left_camera_info_topic, self.left_info_cb, 1)
        self.right_info_sub = self.create_subscription(CameraInfo, self.right_camera_info_topic, self.right_info_cb, 1)

        # subscribes to Image data ROS topics for left and right stereo cameras
        self.left_image_sub = self.create_subscription(Image, self.left_camera_image_topic, self.left_image_cb, 1)
        self.right_image_sub = self.create_subscription(Image, self.right_camera_image_topic, self.right_image_cb, 1)

        self.left_depth_sub = self.create_subscription(PointCloud2, self.left_camera_depth_topic, self.left_depth_cb, 1)
        self.right_depth_sub = self.create_subscription(PointCloud2, self.right_camera_depth_topic, self.right_depth_cb, 1)

    def left_info_cb(self, msg):
        self.left_camera_info = msg

    def right_info_cb(self, msg):
        self.right_camera_info = msg

    def left_image_cb(self, msg):
        self.left_image = msg

        # if self.l_count[0] < 1:  # Save only the first image
        #     cv_img = self.cv_bridge.imgmsg_to_cv2(self.left_image, desired_encoding='passthrough') # converts ROS Image message to OpenCV image format
        #     fname = f'/home/dvrk-team/internship/compvis/images/StereoL.png'
        #     cv.imwrite(fname, cv_img) # saves the OpenCV image to a file
        #     self.get_logger().info(f'Image saved to {fname}')
        #     self.l_count[0] += 1
        # else:
        #     self.get_logger().info('Left image already saved, skipping.')


    def right_image_cb(self, msg):
        self.right_image = msg

        # if self.r_count[0] < 1:  # Save only the first image
        #     cv_img = self.cv_bridge.imgmsg_to_cv2(self.right_image, desired_encoding='passthrough') # converts ROS Image message to OpenCV image format
        #     fname = f'/home/dvrk-team/internship/compvis/images/StereoR.png'
        #     cv.imwrite(fname, cv_img) # saves the OpenCV image to a file
        #     self.get_logger().info(f'Image saved to {fname}')
        #     self.r_count[0] += 1
        # else:
        #     self.get_logger().info('Right image already saved, skipping.')  


    def left_depth_cb(self, msg):
        self.left_depth = msg

        points = point_cloud2.read_points(
        msg,
        field_names=("x", "y", "z", "rgb"),
        skip_nans=True,
        )

        xyz = np.column_stack((points["x"], points["y"], points["z"], points["rgb"])).astype(np.float32)

        fname = f'/home/dvrk-team/Desktop/pointcloudL_curr.npy' # save to .npy file for jupyter notebook processing
        
        np.save(fname, xyz)

        self.get_logger().info('left depth data logged')

    def right_depth_cb(self, msg):
        self.right_depth = msg


# ROS2 entry point
def main(args=None):
    rclpy.init(args=args)
    
    # Runs init
    node = CameraInterface()
 
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
