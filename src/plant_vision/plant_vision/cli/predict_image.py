"""Predict the flower class of one image."""

import argparse

import torch
from PIL import Image

from plant_vision.inference import get_class_names, load_model, predict


def predict_file(image_path, model, class_names, device):
    image = Image.open(image_path)
    results = predict(
        model=model,
        image=image,
        class_names=class_names,
        device=device,
        top_k=5,
    )

    print()
    print("===================================")
    print("PREDICTION")
    print("===================================")
    best = results[0]
    print(f"Prediction: {best['class_name']}")
    print(f"Confidence: {best['confidence']:.2%}")
    print()
    print("Top 5:")

    for result in results:
        print(f"{result['class_name']:30s} {result['confidence']:.2%}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=str, help="Path to image")
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Device:", device)
    model = load_model(device)
    class_names = get_class_names()
    predict_file(args.image, model, class_names, device)


if __name__ == "__main__":
    main()
