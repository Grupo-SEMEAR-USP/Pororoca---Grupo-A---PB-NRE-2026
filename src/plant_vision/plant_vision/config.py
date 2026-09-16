"""Central project paths and runtime configuration."""

import os
from dataclasses import dataclass
from pathlib import Path


def _workspace_root() -> Path:
    """Resolve the workspace root in source and installed environments."""
    configured_root = os.environ.get("WALLYNGTON_WORKSPACE_ROOT")
    if configured_root:
        return Path(configured_root).expanduser().resolve()

    source_root = Path(__file__).resolve().parents[3]
    if (source_root / "src" / "plant_vision").is_dir():
        return source_root

    return Path.cwd().resolve()


def _runtime_path(environment_variable: str, default: Path) -> Path:
    configured_path = os.environ.get(environment_variable)
    if configured_path:
        return Path(configured_path).expanduser().resolve()
    return default


PROJECT_ROOT = _workspace_root()
DATA_DIR = _runtime_path("WALLYNGTON_VISION_DATA_DIR", PROJECT_ROOT / "data")
MODELS_DIR = _runtime_path("WALLYNGTON_VISION_MODELS_DIR", PROJECT_ROOT / "models")
RESULTS_DIR = _runtime_path("WALLYNGTON_VISION_RESULTS_DIR", PROJECT_ROOT / "results")
CHECKPOINT_PATH = _runtime_path(
    "WALLYNGTON_VISION_CHECKPOINT",
    MODELS_DIR / "best_model.pt",
)


@dataclass(frozen=True)
class ModelConfig:
    num_classes: int = 102
    image_size: int = 224


@dataclass(frozen=True)
class TrainingConfig:
    batch_size: int = 32
    warmup_epochs: int = 5
    finetune_epochs: int = 15
    warmup_lr: float = 1e-3
    backbone_lr: float = 1e-4
    classifier_lr: float = 5e-4
    weight_decay: float = 1e-4


@dataclass(frozen=True)
class CameraConfig:
    camera_index: int = 0
    inference_every_n_frames: int = 5


@dataclass(frozen=True)
class TagDetectionConfig:
    min_area: float = 1000.0
    lower_yellow: tuple[int, int, int] = (15, 200, 100)
    upper_yellow: tuple[int, int, int] = (35, 255, 255)
    min_aspect_ratio: float = 0.5
    max_aspect_ratio: float = 2.0
    kernel_size: int = 5
    min_circularity: float = 0.2


MODEL_CONFIG = ModelConfig()
TRAINING_CONFIG = TrainingConfig()
CAMERA_CONFIG = CameraConfig()
TAG_DETECTION_CONFIG = TagDetectionConfig()
