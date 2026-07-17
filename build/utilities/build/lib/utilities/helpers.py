import numpy as np

from geometry_msgs.msg import PoseStamped
from ambf_msgs.msg import RigidBodyState


from PyKDL import Vector, Rotation, Frame


def quat_to_rpy(q1,q2,q3,q4): # Custom quaternion to RPY function (equations in https://www.vcalc.com/wiki/quaternion-to-roll-pitch-yaw)
    roll = np.arctan2(2*((q4*q1)+(q2*q3)), (1-2*(np.power(q1,2)+np.power(q2,2))))
    pitch = np.arcsin(2*((q4*q2)-(q3*q1)))
    yaw = np.arctan2(2*((q4*q3)+(q1*q2)), (1-2*(np.power(q2,2)+np.power(q3,2))))

    return roll, pitch, yaw

# convert PoseStamped to frame
def ps_to_frame(ps: PoseStamped):
    position = Vector(ps.pose.position.x, ps.pose.position.y, ps.pose.position.z)
    
    roll, pitch, yaw = quat_to_rpy(ps.pose.orientation.x,ps.pose.orientation.y,ps.pose.orientation.z,ps.pose.orientation.w)
    rotation = Rotation.RPY(roll, pitch, yaw)

    return Frame(rotation, position)


# convert RigidBodyState to frame
def rbs_to_frame(rbs: RigidBodyState):
    # position to vector
    object_position = Vector(rbs.pose.position.x, rbs.pose.position.y, rbs.pose.position.z)
    
    # convert orientation quaternion to RPY
    roll, pitch, yaw = quat_to_rpy(rbs.pose.orientation.x, rbs.pose.orientation.y, rbs.pose.orientation.z, rbs.pose.orientation.w)
    object_rotation = Rotation.RPY(roll, pitch,yaw)

    # Receives RigidBodyPose, Returns Frame
    return Frame(object_rotation, object_position)
