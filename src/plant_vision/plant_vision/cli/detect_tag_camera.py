"""Run yellow-tag detection from a local webcam."""

import cv2

from plant_vision.config import CAMERA_CONFIG
from plant_vision.vision import (
    annotate_detections,
    create_yellow_mask,
    detect_tag_contours,
)


def main():
    camera = cv2.VideoCapture(CAMERA_CONFIG.camera_index)
    if not camera.isOpened():
        raise RuntimeError("Erro ao abrir a câmera.")

    try:
        while True:
            success, frame = camera.read()
            if not success:
                print("Erro ao capturar o frame.")
                break

            mask = create_yellow_mask(frame)
            detections = detect_tag_contours(mask)

            for detection in detections:
                print(
                    "| Area:", detection.area,
                    "| Perimetro:", detection.perimeter,
                    "| proporcao:", detection.aspect_ratio,
                    "| circularidade:", detection.circularity,
                )

            annotated = annotate_detections(frame, detections)
            cv2.imshow("Contornos Filtrados", annotated)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
