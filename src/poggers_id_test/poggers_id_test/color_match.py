import rclpy
import cv2
from rclpy.node import Node
from cv_bridge import CvBridge
import numpy as np

from sensor_msgs.msg import Image
from wallington_interfaces.srv import VisionRequest

class color_match_node(Node):
    def __init__(self):
        super().__init__("color_match")
        self.bridge = CvBridge()
        self.current_frame = None
        self.subscriber = self.create_subscription(Image, "/camera", self.callback_image, 10)
        self.detection_server = self.create_service(VisionRequest, "tag_identification", self.callback_tag_id)
        self.get_logger().info("Display started!")

    def callback_image(self, img):
        self.current_frame = self.bridge.imgmsg_to_cv2(img, desired_encoding='bgr8')

        cv2.imshow("Gazebo Camera Feed", self.current_frame)
        cv2.waitKey(1)

    def callback_tag_id(self, request, response):
        hsv_image = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2HSV)

        mask = None
        if(request.color == 'red'):
            lower_red_1 = np.array([0, 100, 100])
            upper_red_1 = np.array([10, 255, 255])
            
            lower_red_2 = np.array([170, 100, 100])
            upper_red_2 = np.array([180, 255, 255])

            mask1 = cv2.inRange(hsv_image, lower_red_1, upper_red_1)
            mask2 = cv2.inRange(hsv_image, lower_red_2, upper_red_2)
            mask = cv2.bitwise_or(mask1, mask2)
        elif(request.color == 'blue'):
            lower_blue = np.array([100, 150, 0])
            upper_blue = np.array([140, 255, 255])

            mask = cv2.inRange(hsv_image, lower_blue, upper_blue)
        elif(request.color == 'yellow'):
            lower_yellow = np.array([20, 100, 100])
            upper_yellow = np.array([30, 255, 255])

            mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)

        found_color = cv2.countNonZero(mask) > 0
        self.get_logger().info('Verification complete!')
        response.answer = found_color
        return response


def main(args=None):
    rclpy.init(args=args)
    myNode = color_match_node()
    rclpy.spin(myNode)
    rclpy.shutdown()

if __name__=="__main__":
    main()