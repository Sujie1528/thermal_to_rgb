import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np

bridge = CvBridge()
count = 0

def callback(image_msg):
    global count
   
    cv_image = bridge.imgmsg_to_cv2(image_msg, "32FC1")
    print(cv_image.shape)
    height, width = cv_image.shape
    total = width * height
    print(cv_image)
    while np.count_nonzero(~np.isnan(cv_image)) != total:
        for i in range(height):
            for j in range(width):
                if np.isnan(cv_image[i, j]):
                    up_bound = max(0, i - 2)
                    bottom_bound = min(i+2, height)
                    right_bound = max(0, j-2)
                    left_bound = min(j+2, width)
                    sum = 0
                    count = 0
                    for m in range(up_bound, bottom_bound):
                        for n in range(right_bound, left_bound):
                            if not np.isnan(cv_image[m, n]):
                                sum += cv_image[m, n]
                                count += 1
                    if sum > 0:
                        cv_image[i, j] = sum / count


    print(cv_image)
    #print(cv_image.shape)
    #print(mask.shape)
    
  


def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("/camera/depth_registered/sw_registered/image_rect/", Image, callback)
    #rospy.Subscriber("/camera/depth/image/", Image, callback)

    # spin() simply keeps python from exiting until this node is stopped
    while not rospy.is_shutdown():
        rospy.spin()

if __name__ == '__main__':
    listener()