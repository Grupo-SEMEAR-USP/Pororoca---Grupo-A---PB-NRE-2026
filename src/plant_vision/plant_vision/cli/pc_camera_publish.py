import rclpy
from rclpy.node import Node

import cv2
from cv_bridge import CvBridge

from sensor_msgs.msg import Image

class pc_camera_publish(Node):
    def __init__(self):
        super().__init__("pc_camera_publish")
        self.publisher = self.create_publisher(Image, "/camera", 10)
        self.bridge = CvBridge()
        self.timer = self.create_timer(0.05, self.publish_callback)
        self.camera = cv2.VideoCapture(0)

    def publish_callback(self):
        success, frame = self.camera.read()
        image = self.bridge.cv2_to_imgmsg(frame)
        self.publisher.publish(image)

    def destroy_node(self):
        self.camera.release()

def main(args=None):
    rclpy.init(args=args)
    myNode = pc_camera_publish()
    rclpy.spin(myNode)
    cv2.destroyAllWindows()
    myNode.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
