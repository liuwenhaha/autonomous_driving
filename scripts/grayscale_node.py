#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy

from imagepreprocessing import ImagePreparator
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

NODE_NAME = "grayscale_node"
SUB_TOPIC = "image"
PUB_TOPIC = "image_preproc_grayscale"
QUEUE_SIZE = 1


class GrayscaleNode:

    def __init__(self, node_name, sub_topic, pub_topic):
        self.bridge = CvBridge()
        self.img_prep = ImagePreparator()
        
        self.image_pub = rospy.Publisher(pub_topic, Image, queue_size=QUEUE_SIZE)

        rospy.init_node(node_name, anonymous=True)

        self.image_sub = rospy.Subscriber(sub_topic, Image, self.callback)

        rospy.spin()

    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(e)

        gray = self.img_prep.grayscale(cv_image)

        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(gray, "mono8"))
        except CvBridgeError as e:
            rospy.logerr(e)


def main():
    try:
        GrayscaleNode(NODE_NAME, SUB_TOPIC, PUB_TOPIC)
    except KeyboardInterrupt:
        rospy.loginfo("Shutting down node %s", NODE_NAME)

if __name__ == '__main__':
    main()
