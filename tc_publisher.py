#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image

from pithermalcam.pi_therm_cam import pithermalcam
from pithermalcam2.modded_pi_therm_cam import pithermalcam as pithermalcam2
from cv_bridge import CvBridge
import cv2
import cmapy

SENSOR_TOPIC = "tc_data"
SENSOR_TOPIC2 = "tc2_data"


def setup():
    global pub, pub2, rate, cam, cam2
    pub = rospy.Publisher(SENSOR_TOPIC, Image, queue_size=1)
    pub2 = rospy.Publisher(SENSOR_TOPIC2, Image, queue_size=1)
    rospy.init_node("camera_serial")
    rate = rospy.Rate(10)  # 10hz

    # Set up camera
    cam = pithermalcam()
    cam2 = pithermalcam2()

    # Set the interpolation to Scipy/CV2 Mixed
    cam._interpolation_index = 6
    cam2._interpolation_index = 6

    # Set the colormap to seismic
    cam._colormap_index = 2
    cam2._colormap_index = 2


def loop():
    # Update the image to the latest frame from camera
    cam_data = cam.update_image_frame()
    cam2._pull_raw_image()
    cam_data2 = cv2.applyColorMap(cam2._raw_image, cmapy.cmap("seismic"))
    print(cam2._raw_image)

    bridge = CvBridge()
    image_msg = bridge.cv2_to_imgmsg(cam_data, encoding="passthrough")
    image_msg2 = bridge.cv2_to_imgmsg(cam_data2, encoding="passthrough")

    pub.publish(image_msg)
    pub2.publish(image_msg2)
    rate.sleep()


if __name__ == "__main__":
    try:
        setup()
        while not rospy.is_shutdown():
            loop()
    except rospy.ROSInterruptException as e:
        print(e)
        pass
