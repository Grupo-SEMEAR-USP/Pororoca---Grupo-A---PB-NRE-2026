"""Evaluate the best Flowers102 checkpoint."""

import torch

from plant_vision.config import RESULTS_DIR, TRAINING_CONFIG
from plant_vision.data import create_dataloaders
from plant_vision.evaluation.evaluator import evaluate, load_best_model
from plant_vision.evaluation.metrics import (
    analyze_confidence,
    get_classification_report,
    print_best_classes,
    print_high_confidence_errors,
    print_metrics,
    print_top_confusions,
    print_worst_classes,
)
from plant_vision.evaluation.visualization import (
    plot_normalized_confusion_matrix,
    visualize_errors,
    visualize_high_confidence_errors,
)


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Device:", device)

    print("Loading Best Model...")
    model = load_best_model(device)
    _, _, test_loader = create_dataloaders(TRAINING_CONFIG.batch_size)
    print(f"Number of tests: {len(test_loader.dataset)}")

    class_names = test_loader.dataset.classes
    print("Número de classes:", len(class_names))
    print("Primeiras 5 classes:", class_names[:5])

    print("Evaluating Model...")
    test_loss, labels, predictions, confidences, errors = evaluate(
        model,
        test_loader,
        device,
    )

    print_metrics(test_loss, labels, predictions)
    print_top_confusions(labels, predictions, class_names, top_k=10)
    report = get_classification_report(labels, predictions, class_names)
    print_best_classes(report, class_names)
    print_worst_classes(report, class_names)
    analyze_confidence(labels, predictions, confidences)
    print_high_confidence_errors(errors, class_names)
    visualize_errors(test_loader.dataset, errors, class_names)
    visualize_high_confidence_errors(test_loader.dataset, errors, class_names)
    plot_normalized_confusion_matrix(labels, predictions, len(class_names))


if __name__ == "__main__":
    main()
