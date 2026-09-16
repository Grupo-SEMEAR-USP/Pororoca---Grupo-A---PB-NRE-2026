"""Model loading, preprocessing, and prediction."""

from pathlib import Path

import torch

from plant_vision.config import CHECKPOINT_PATH
from plant_vision.data import FLOWERS102_CLASSES, eval_transform
from plant_vision.models import create_model


def load_model(device, checkpoint_path: str | Path = CHECKPOINT_PATH):
    model = create_model(pretrained=False).to(device)
    checkpoint = torch.load(
        checkpoint_path,
        map_location=device,
        weights_only=True,
    )
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    return model


def get_class_names() -> list[str]:
    """Return class labels without downloading or loading the dataset."""
    return list(FLOWERS102_CLASSES)


def preprocess_image(image):
    image = image.convert("RGB")
    return eval_transform(image).unsqueeze(0)


def predict(model, image, class_names, device, top_k: int = 5):
    tensor = preprocess_image(image).to(device, non_blocking=True)

    with torch.inference_mode():
        logits = model(tensor)
        probabilities = torch.softmax(logits.float(), dim=1)

    top_probabilities, top_indices = torch.topk(
        probabilities,
        k=top_k,
        dim=1,
    )

    results = []
    for probability, index in zip(
        top_probabilities[0].cpu().tolist(),
        top_indices[0].cpu().tolist(),
    ):
        results.append(
            {
                "class_id": index,
                "class_name": class_names[index],
                "confidence": probability,
            }
        )

    return results
