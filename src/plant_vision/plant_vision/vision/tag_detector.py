"""Yellow-tag segmentation and contour filtering."""

from dataclasses import dataclass

import cv2
import numpy as np

from plant_vision.config import TAG_DETECTION_CONFIG, TagDetectionConfig


@dataclass(frozen=True)
class TagDetection:
    contour: np.ndarray
    x: int
    y: int
    width: int
    height: int
    area: float
    perimeter: float
    aspect_ratio: float
    circularity: float


def create_yellow_mask(
    frame: np.ndarray,
    config: TagDetectionConfig = TAG_DETECTION_CONFIG,
) -> np.ndarray:
    """Segment yellow regions and clean the mask morphologically."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(
        hsv,
        np.array(config.lower_yellow),
        np.array(config.upper_yellow),
    )
    kernel = np.ones((config.kernel_size, config.kernel_size), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    return cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)


def detect_tag_contours(
    mask: np.ndarray,
    config: TagDetectionConfig = TAG_DETECTION_CONFIG,
) -> list[TagDetection]:
    """Return contours that match the original tag geometry filters."""
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )
    detections = []

    for contour in contours:
        x, y, width, height = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)
        aspect_ratio = width / float(height)
        perimeter = cv2.arcLength(contour, True)

        if perimeter == 0:
            continue

        circularity = 4 * np.pi * (area / (perimeter**2))
        matches = (
            area > config.min_area
            and config.min_aspect_ratio < aspect_ratio < config.max_aspect_ratio
            and circularity > config.min_circularity
        )

        if matches:
            detections.append(
                TagDetection(
                    contour=contour,
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    area=area,
                    perimeter=perimeter,
                    aspect_ratio=aspect_ratio,
                    circularity=circularity,
                )
            )

    return detections


def annotate_detections(
    frame: np.ndarray,
    detections: list[TagDetection],
) -> np.ndarray:
    """Draw the same contour, box, and circularity annotation as before."""
    annotated = frame.copy()

    for detection in detections:
        cv2.drawContours(annotated, [detection.contour], -1, (0, 255, 0), 2)
        cv2.rectangle(
            annotated,
            (detection.x, detection.y),
            (
                detection.x + detection.width,
                detection.y + detection.height,
            ),
            (255, 0, 0),
            2,
        )
        cv2.putText(
            annotated,
            f"Circularidade: {detection.circularity:.2f}",
            (detection.x, detection.y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )

    return annotated
