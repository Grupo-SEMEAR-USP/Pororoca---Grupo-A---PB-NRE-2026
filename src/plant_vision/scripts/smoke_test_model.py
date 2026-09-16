"""Run a simple model shape smoke check."""

import torch
from plant_vision.config import MODEL_CONFIG
from plant_vision.models import create_model


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Device:", device)

    model = create_model(pretrained=False).to(device)
    model.eval()
    images = torch.randn(
        4,
        3,
        MODEL_CONFIG.image_size,
        MODEL_CONFIG.image_size,
        device=device,
    )

    with torch.no_grad():
        outputs = model(images)

    print()
    print("Input:")
    print(images.shape)
    print()
    print("Output:")
    print(outputs.shape)


if __name__ == "__main__":
    main()
