"""Flowers102 datasets, transforms, and dataloaders."""

from pathlib import Path

import torch
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.datasets import Flowers102

from plant_vision.config import DATA_DIR, MODEL_CONFIG, TRAINING_CONFIG

IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

train_transform = transforms.Compose(
    [
        transforms.RandomResizedCrop(MODEL_CONFIG.image_size),
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ]
)

eval_transform = transforms.Compose(
    [
        transforms.Resize(256),
        transforms.CenterCrop(MODEL_CONFIG.image_size),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ]
)


def create_datasets(root: str | Path = DATA_DIR):
    """Create the train, validation, and test splits of Flowers102."""
    root = str(root)

    train_dataset = Flowers102(
        root=root,
        split="train",
        transform=train_transform,
        download=True,
    )
    val_dataset = Flowers102(
        root=root,
        split="val",
        transform=eval_transform,
        download=True,
    )
    test_dataset = Flowers102(
        root=root,
        split="test",
        transform=eval_transform,
        download=True,
    )

    return train_dataset, val_dataset, test_dataset


def create_dataloaders(
    batch_size: int = TRAINING_CONFIG.batch_size,
    root: str | Path = DATA_DIR,
    num_workers: int = 0,
):
    """Create dataloaders for all Flowers102 splits."""
    train_dataset, val_dataset, test_dataset = create_datasets(root=root)
    pin_memory = torch.cuda.is_available()

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=pin_memory,
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=pin_memory,
    )
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=pin_memory,
    )

    return train_loader, val_loader, test_loader
