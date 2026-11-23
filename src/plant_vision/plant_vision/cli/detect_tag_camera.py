import rclpy
from rclpy.node import Node

import cv2
from cv_bridge import CvBridge

from sensor_msgs.msg import Image
from wallington_interfaces.srv import VisionRequest

from plant_vision.config import CAMERA_CONFIG
from plant_vision.vision import(
    annotate_detections,
    create_yellow_mask,
    detect_tag_contours,
)

class detect_tag_camera(Node):
    def __init__(self):
        super().__init__("detect_tag_camera")
        self.bridge = CvBridge()
        self.frame = None
        self.camera_sub = self.create_subscription(Image, "/camera", self.camera_callback, 10)
        self.detection_server = self.create_service(VisionRequest, "tag_identification", self.tag_detection_callback)
        self.get_logger().info("Tag detection initialized!")

    def camera_callback(self, img):
        self.frame = self.bridge.imgmsg_to_cv2(img)

        #Note: the following code is NOT NEEDED to run. It is solely for TEST PURPOSES!!
        mask = create_yellow_mask(self.frame)
        detections = detect_tag_contours(mask)

        for detection in detections:
            self.get_logger().info(
                "| Area:" + str(detection.area) +
                "| Perimetro:" + str(detection.perimeter) +
                "| proporcao:" + str(detection.aspect_ratio,) +
                "| circularidade:"+ str(detection.circularity)
            )

        annotated = annotate_detections(self.frame, detections)
        cv2.imshow("Contornos Filtrados", annotated)
        cv2.waitKey(1)

    def tag_detection_callback(self, request, response):
        mask = create_yellow_mask(self.frame)
        detections = detect_tag_contours(mask)
        detection_count = 0

        for detection in detections:
            self.get_logger().info(
                "| Area:", detection.area,
                "| Perimetro:", detection.perimeter,
                "| proporcao:", detection.aspect_ratio,
                "| circularidade:", detection.circularity,
            )
            if(detection.circularity>=0.7):
                detection_count += 1

        annotated = annotate_detections(self.frame, detections)
        cv2.imshow("Contornos Filtrados", annotated)

        response.answer = detection_count > 0
        return response

def main(args = None):
    rclpy.init(args=args)
    myNode = detect_tag_camera()
    rclpy.spin(myNode)
    cv2.destroyAllWindows()
    rclpy.shutdown()

if __name__ == "__main__":
    main()