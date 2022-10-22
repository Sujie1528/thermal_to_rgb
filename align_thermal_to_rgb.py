import pyrealsense2 as rs
import rospy
import message_filters
from sensor_msgs.msg import Image, CameraInfo


rgb_intrinsics = rs.intrinsics()
thermal_intrinsics = rs.intrinsics()


def find_correspondence(pixel, extrinsics_from_rgb_to_thermal):
    depth = 0 #TODO: retrieve the depth based on registered_depth_image
    rgb_point = rs.rs2_deproject_pixel_to_point(rgb_intrinsics, pixel, depth)
    thermal_point = rs.rs2_transform_point_to_point(extrinsics_from_rgb_to_thermal, rgb_point)
    thermal_pixel = rs.rs2_project_point_to_pixel(thermal_intrinsics, thermal_point)


def align():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('align_thermal_to_rgb', anonymous=True)
    image_sub = message_filters.Subscriber('image', Image)
    info_sub = message_filters.Subscriber('camera_info', CameraInfo)

    ts = message_filters.TimeSynchronizer([image_sub, info_sub], 10)
    ts.registerCallback(callback)
    rospy.spin()
   

    # spin() simply keeps python from exiting until this node is stopped
    while not rospy.is_shutdown():
        rospy.spin()



def callback(image, camera_info):
  # Solve all of perception here...

image_sub = message_filters.Subscriber('image', Image)
info_sub = message_filters.Subscriber('camera_info', CameraInfo)

ts = message_filters.TimeSynchronizer([image_sub, info_sub], 10)
ts.registerCallback(callback)
rospy.spin()