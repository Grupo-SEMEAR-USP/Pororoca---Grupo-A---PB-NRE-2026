"""Train the Flowers102 classifier in two stages."""

import torch
from torch import nn
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR

from plant_vision.config import CHECKPOINT_PATH, TRAINING_CONFIG
from plant_vision.data import create_dataloaders
from plant_vision.models import create_model, freeze_backbone, unfreeze_all
from plant_vision.training import fit_stage


def main():
    config = TRAINING_CONFIG
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Device:", device)

    train_loader, val_loader, _ = create_dataloaders(
        batch_size=config.batch_size
    )
    model = create_model(pretrained=True).to(device)
    criterion = nn.CrossEntropyLoss()
    scaler = torch.amp.GradScaler("cuda", enabled=device.type == "cuda")
    best_val_accuracy = 0.0

    print()
    print("===================================")
    print("STAGE 1 - CLASSIFIER WARM-UP")
    print("===================================")

    freeze_backbone(model)
    trainable_params = sum(
        parameter.numel()
        for parameter in model.parameters()
        if parameter.requires_grad
    )
    total_params = sum(parameter.numel() for parameter in model.parameters())
    print(f"Trainable parameters: {trainable_params:,} / {total_params:,}")

    optimizer = AdamW(
        filter(lambda parameter: parameter.requires_grad, model.parameters()),
        lr=config.warmup_lr,
        weight_decay=config.weight_decay,
    )
    scheduler = CosineAnnealingLR(
        optimizer,
        T_max=config.warmup_epochs,
    )
    best_val_accuracy = fit_stage(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        criterion=criterion,
        optimizer=optimizer,
        scheduler=scheduler,
        device=device,
        scaler=scaler,
        epochs=config.warmup_epochs,
        stage_name="warmup",
        best_val_accuracy=best_val_accuracy,
        checkpoint_path=CHECKPOINT_PATH,
        freeze_backbone_bn=True,
    )

    print()
    print("===================================")
    print("STAGE 2 - FULL FINE-TUNING")
    print("===================================")

    unfreeze_all(model)
    optimizer = AdamW(
        [
            {
                "params": model.features.parameters(),
                "lr": config.backbone_lr,
            },
            {
                "params": model.classifier.parameters(),
                "lr": config.classifier_lr,
            },
        ],
        weight_decay=config.weight_decay,
    )
    scheduler = CosineAnnealingLR(
        optimizer,
        T_max=config.finetune_epochs,
    )
    best_val_accuracy = fit_stage(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        criterion=criterion,
        optimizer=optimizer,
        scheduler=scheduler,
        device=device,
        scaler=scaler,
        epochs=config.finetune_epochs,
        stage_name="finetune",
        best_val_accuracy=best_val_accuracy,
        checkpoint_path=CHECKPOINT_PATH,
        freeze_backbone_bn=False,
    )

    print()
    print(
        "Treinamento concluído. "
        f"Melhor validation accuracy: {best_val_accuracy:.2%}"
    )


if __name__ == "__main__":
    main()
