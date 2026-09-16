"""Run flower classification from a local webcam."""

import time

import cv2
import torch
from PIL import Image

from plant_vision.config import CAMERA_CONFIG
from plant_vision.inference import get_class_names, load_model, predict


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Device:", device)
    print("Loading model...")

    model = load_model(device)
    class_names = get_class_names()

    print("Opening camera...")
    camera = cv2.VideoCapture(CAMERA_CONFIG.camera_index)
    if not camera.isOpened():
        raise RuntimeError("Could not open camera.")

    frame_number = 0
    last_results = None
    last_inference_ms = 0.0

    print("Camera running.")
    print("Press Q to quit.")

    while True:
        success, frame = camera.read()
        if not success:
            print("Could not read frame.")
            break

        if frame_number % CAMERA_CONFIG.inference_every_n_frames == 0:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)
            start = time.perf_counter()
            last_results = predict(
                model=model,
                image=image,
                class_names=class_names,
                device=device,
                top_k=3,
            )
            last_inference_ms = (time.perf_counter() - start) * 1000

        if last_results:
            best = last_results[0]
            prediction_text = (
                f"{best['class_name']} {best['confidence']:.1%}"
            )
            cv2.putText(
                frame,
                prediction_text,
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )
            cv2.putText(
                frame,
                f"Inference: {last_inference_ms:.1f} ms",
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )

            y_position = 110
            for rank, result in enumerate(last_results, start=1):
                text = (
                    f"{rank}. {result['class_name']} "
                    f"{result['confidence']:.1%}"
                )
                cv2.putText(
                    frame,
                    text,
                    (20, y_position),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (255, 255, 255),
                    1,
                    cv2.LINE_AA,
                )
                y_position += 27

        cv2.imshow("Plant Classifier", frame)
        frame_number += 1
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
