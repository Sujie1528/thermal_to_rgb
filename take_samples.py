import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import os

# ROS Image message -> OpenCV2 image converter
bridge = CvBridge()


def main():
    index = "00"

    # Path to save the files
    path = os.path.join(os.path.dirname(__file__), "samples")
    if not os.path.isdir(path):
        os.makedirs(path)
        print("Created directory: " + path)

    # Initialize node and set topic
    rospy.init_node("cam_data_sampler")

    # Declare ROS topic names for each camera
    tc_topic = "tc_data"
    tc2_topic = "tc2_data"
    overhead_rsc_topic = "overhead_rsc/color/image_raw"
    arm_rsc_topic = "camera/color/image_raw"

    while True:
        # Wait for user input
        input(f"Click enter to take image! Current index: {index}")

        # Get message
        tc_msg = rospy.wait_for_message(tc_topic, Image)
        tc2_msg = rospy.wait_for_message(tc2_topic, Image)
        overhead_rsc_msg = rospy.wait_for_message(overhead_rsc_topic, Image)
        arm_rsc_msg = rospy.wait_for_message(arm_rsc_topic, Image)

        try:
            # Convert your ROS Image message to OpenCV2
            cv2_tc_img = bridge.imgmsg_to_cv2(tc_msg,
                                              desired_encoding="passthrough")
            cv2_tc2_img = bridge.imgmsg_to_cv2(tc2_msg,
                                               desired_encoding="passthrough")
            cv2_overhead_rsc_img = bridge.imgmsg_to_cv2(overhead_rsc_msg,
                                                        desired_encoding="bgr8")
            cv2_arm_rsc_img = bridge.imgmsg_to_cv2(arm_rsc_msg,
                                                   desired_encoding="bgr8")
        except CvBridgeError as e:
            print(e)
            continue

        # Save your OpenCV2 image as a png
        tc_fn = os.path.join(path, "tc_" + index + ".png")
        tc2_fn = os.path.join(path, "tc2_" + index + ".png")
        overhead_rsc_fn = os.path.join(path, "oc_" + index + ".png")
        arm_rsc_fn = os.path.join(path, "ac_" + index + ".png")

        cv2.imwrite(tc_fn, cv2_tc_img)
        cv2.imwrite(tc2_fn, cv2_tc2_img)
        cv2.imwrite(overhead_rsc_fn, cv2_overhead_rsc_img)
        cv2.imwrite(arm_rsc_fn, cv2_arm_rsc_img)

        # Increment index with leading zeros
        index = str(int(index) + 1).zfill(len(index))


if __name__ == '__main__':
    main()
