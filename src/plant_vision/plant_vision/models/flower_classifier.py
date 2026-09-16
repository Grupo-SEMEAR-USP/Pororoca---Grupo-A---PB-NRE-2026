"""MobileNetV3 model used for Flowers102 classification."""

from torch import nn
from torchvision.models import MobileNet_V3_Small_Weights, mobilenet_v3_small

from plant_vision.config import MODEL_CONFIG


def create_model(
    num_classes: int = MODEL_CONFIG.num_classes,
    pretrained: bool = True,
):
    """Create MobileNetV3 Small with a classifier for ``num_classes``."""
    weights = MobileNet_V3_Small_Weights.DEFAULT if pretrained else None
    model = mobilenet_v3_small(weights=weights)
    in_features = model.classifier[-1].in_features
    model.classifier[-1] = nn.Linear(in_features, num_classes)
    return model


def freeze_backbone(model) -> None:
    """Freeze all parameters except the final classifier layer."""
    for parameter in model.parameters():
        parameter.requires_grad = False

    for parameter in model.classifier[-1].parameters():
        parameter.requires_grad = True


def unfreeze_all(model) -> None:
    """Enable training for every model parameter."""
    for parameter in model.parameters():
        parameter.requires_grad = True
