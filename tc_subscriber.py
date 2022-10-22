import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

bridge = CvBridge()

def callback(image_msg):
    data = bridge.imgmsg_to_cv2(image_msg, desired_encoding='passthrough')
    #rospy.loginfo(rospy.get_caller_id() + 'I heard %s', repr(data))
    cv2.imshow("image", data)
    cv2.waitKey(10)

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("tc_data", Image, callback)

    # spin() simply keeps python from exiting until this node is stopped
    while not rospy.is_shutdown():
        rospy.spin()

if __name__ == '__main__':
    listener()
