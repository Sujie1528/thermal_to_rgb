import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np
from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2

bridge = CvBridge()
count = 0

def callback(points):
    global count
    if count == 0:
        gen = point_cloud2.read_points(points)
        print(type(gen))
        for p in gen:
            print (p) 
        count += 1
    #print(cv_image.shape)
    #print(mask.shape)
    
  


def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('point_cloud_listener', anonymous=True)

    rospy.Subscriber("/camera/depth_registered/points", PointCloud2, callback)
    #rospy.Subscriber("/camera/depth/image/", Image, callback)

    # spin() simply keeps python from exiting until this node is stopped
    while not rospy.is_shutdown():
        rospy.spin()

if __name__ == '__main__':
    listener()