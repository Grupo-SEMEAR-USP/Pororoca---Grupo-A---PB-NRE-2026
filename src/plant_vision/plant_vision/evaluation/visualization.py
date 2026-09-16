"""Evaluation plots and error visualizations."""

import random
from pathlib import Path

import matplotlib.pyplot as plt
import torch
from sklearn.metrics import confusion_matrix

from plant_vision.config import RESULTS_DIR
from plant_vision.data import IMAGENET_MEAN, IMAGENET_STD


def denormalize_image(image):
    mean = torch.tensor(IMAGENET_MEAN).view(3, 1, 1)
    std = torch.tensor(IMAGENET_STD).view(3, 1, 1)
    image = image.cpu()
    return torch.clamp(image * std + mean, 0, 1)


def visualize_errors(
    dataset,
    errors,
    class_names,
    n: int = 12,
    filename: str | Path = RESULTS_DIR / "random_errors.png",
    randomize: bool = True,
):
    selected = (
        random.sample(errors, min(n, len(errors)))
        if randomize
        else errors[:n]
    )

    if not selected:
        print("No classification errors to visualize.")
        return

    rows = 3
    cols = 4
    fig, axes = plt.subplots(rows, cols, figsize=(15, 11))

    for axis in axes.flat:
        axis.axis("off")

    for axis, error in zip(axes.flat, selected):
        image, _ = dataset[error["index"]]
        image = denormalize_image(image).permute(1, 2, 0)
        axis.imshow(image)
        true_name = class_names[error["true"]]
        predicted_name = class_names[error["predicted"]]
        title = (
            f"Real: {true_name}" + chr(10)
            + f"Pred: {predicted_name}" + chr(10)
            + f"Conf: {error['confidence']:.1%}"
        )
        axis.set_title(title, fontsize=9)
        axis.axis("off")

    filename = Path(filename)
    filename.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.show()
    plt.close(fig)


def visualize_high_confidence_errors(dataset, errors, class_names, n: int = 12):
    sorted_errors = sorted(
        errors,
        key=lambda item: item["confidence"],
        reverse=True,
    )
    visualize_errors(
        dataset=dataset,
        errors=sorted_errors[:n],
        class_names=class_names,
        n=n,
        filename=RESULTS_DIR / "high_confidence_errors.png",
        randomize=False,
    )


def plot_normalized_confusion_matrix(
    labels,
    predictions,
    num_classes: int,
    filename: str | Path = RESULTS_DIR / "confusion_matrix_normalized.png",
):
    matrix = confusion_matrix(labels, predictions, normalize="true")
    fig, axis = plt.subplots(figsize=(13, 11))
    image = axis.imshow(matrix, interpolation="nearest", aspect="auto")
    fig.colorbar(image, ax=axis, label="Proporção")
    axis.set_title("Normalized Confusion Matrix")
    axis.set_xlabel("Predicted Class")
    axis.set_ylabel("True Class")

    ticks = list(range(0, num_classes, 10))
    axis.set_xticks(ticks)
    axis.set_yticks(ticks)
    axis.set_xticklabels(ticks)
    axis.set_yticklabels(ticks)

    filename = Path(filename)
    filename.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(filename, dpi=200)
    plt.show()
    plt.close(fig)
