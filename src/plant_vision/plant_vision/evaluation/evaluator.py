"""Model evaluation and prediction collection."""

from pathlib import Path

import torch
from torch import nn

from plant_vision.config import CHECKPOINT_PATH
from plant_vision.models import create_model


def load_best_model(device, checkpoint_path: str | Path = CHECKPOINT_PATH):
    model = create_model(pretrained=False).to(device)
    checkpoint = torch.load(
        checkpoint_path,
        map_location=device,
        weights_only=True,
    )
    model.load_state_dict(checkpoint["model_state_dict"])
    print(
        f"Checkpoint: {checkpoint['stage']} | "
        f"Val Acc: {checkpoint['val_accuracy']:.2%}"
    )
    return model


def evaluate(model, dataloader, device):
    model.eval()
    criterion = nn.CrossEntropyLoss()
    use_amp = device.type == "cuda"

    total_loss = 0.0
    total_samples = 0
    all_predictions = []
    all_labels = []
    all_confidences = []
    errors = []
    sample_index = 0

    with torch.inference_mode():
        for images, labels in dataloader:
            images = images.to(device, non_blocking=True)
            labels = labels.to(device, non_blocking=True)

            with torch.autocast(
                device_type=device.type,
                dtype=torch.bfloat16,
                enabled=use_amp,
            ):
                batch_size = images.size(0)
                logits = model(images)
                loss = criterion(logits, labels)
                probabilities = torch.softmax(logits.float(), dim=1)
                confidences, predictions = probabilities.max(dim=1)

            labels_cpu = labels.cpu().tolist()
            predictions_cpu = predictions.cpu().tolist()
            confidences_cpu = confidences.cpu().tolist()

            for index in range(batch_size):
                true_label = labels_cpu[index]
                predicted_label = predictions_cpu[index]
                confidence = confidences_cpu[index]

                if predicted_label != true_label:
                    errors.append(
                        {
                            "index": sample_index + index,
                            "true": true_label,
                            "predicted": predicted_label,
                            "confidence": confidence,
                        }
                    )

            sample_index += batch_size
            all_confidences.extend(confidences_cpu)
            total_loss += loss.item() * batch_size
            total_samples += batch_size
            all_predictions.extend(predictions_cpu)
            all_labels.extend(labels_cpu)

    test_loss = total_loss / total_samples
    return test_loss, all_labels, all_predictions, all_confidences, errors
