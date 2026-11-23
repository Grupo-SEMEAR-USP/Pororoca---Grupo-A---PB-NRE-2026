#This code is done, but not tested quite yet! Im still not sure if it works with the full model.

import rclpy
from rclpy.node import Node


import numpy as np

from sensor_msgs.msg import Image as ROSImage
from wallington_interfaces.srv import VisionRequest

import torch
from PIL import Image as PILImage

from plant_vision.inference import get_class_names, load_model, predict

class predict_image(Node):
    def __init__(self):
        super().__init__("predict_image_node")
        self.frame = None
        self.camera_sub = self.create_subscription(ROSImage, "/camera", self.camera_callback, 10)
        self.detection_server = self.create_service(VisionRequest, "plant_identification", self.plant_identification_callback, 10)
        self.get_logger().info("Plant detection initialized!")

    def camera_callback(self, img):
        img_array = np.frombuffer(img.data, dtype=np.uint8).reshape(img.height, img.width, -1)

        if(img.encoding == "bgr8"):
            img_array = img_array[:,:,::-1]

        self.frame = PILImage.fromarray(img_array)

    def plant_identification_callback(self, request, response):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = load_model(device)
        class_names = get_class_names()

        results = predict(
            model=model,
            image=self.frame,
            class_names=class_names,
            device=device,
            top_k=5
        )

        response.answer = False

        for result in results:
            if(result['class_name'] == request.color and result['confidence'] >= 0.7):
                response.answer = True
                break

        return response

def main(args=None):
    rclpy.init(args=args)
    myNode = predict_image()
    rclpy.spin(myNode)
    rclpy.shutdown()

if __name__ == "__main__":
    main()