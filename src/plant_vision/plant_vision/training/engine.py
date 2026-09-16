"""Training and validation loops."""

from pathlib import Path

import torch

from plant_vision.training.checkpoint import save_training_checkpoint


def train_one_epoch(
    model,
    dataloader,
    criterion,
    optimizer,
    scaler,
    device,
    freeze_backbone_bn: bool = False,
):
    model.train()

    if freeze_backbone_bn:
        model.features.eval()

    running_loss = 0.0
    correct = 0
    total = 0
    use_amp = device.type == "cuda"

    for images, labels in dataloader:
        images = images.to(device, non_blocking=True)
        labels = labels.to(device, non_blocking=True)
        optimizer.zero_grad(set_to_none=True)

        with torch.autocast(
            device_type=device.type,
            dtype=torch.float16,
            enabled=use_amp,
        ):
            logits = model(images)
            loss = criterion(logits, labels)

        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()

        batch_size = images.size(0)
        running_loss += loss.item() * batch_size
        predictions = logits.argmax(dim=1)
        correct += (predictions == labels).sum().item()
        total += batch_size

    return running_loss / total, correct / total


@torch.inference_mode()
def validate_one_epoch(model, dataloader, criterion, device):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    use_amp = device.type == "cuda"

    for images, labels in dataloader:
        images = images.to(device, non_blocking=True)
        labels = labels.to(device, non_blocking=True)

        with torch.autocast(
            device_type=device.type,
            dtype=torch.float16,
            enabled=use_amp,
        ):
            logits = model(images)
            loss = criterion(logits, labels)

        predictions = logits.argmax(dim=1)
        batch_size = images.size(0)
        running_loss += loss.item() * batch_size
        correct += (predictions == labels).sum().item()
        total += batch_size

    return running_loss / total, correct / total


def fit_stage(
    model,
    train_loader,
    val_loader,
    criterion,
    optimizer,
    scheduler,
    device,
    scaler,
    epochs: int,
    stage_name: str,
    best_val_accuracy: float,
    checkpoint_path: str | Path,
    freeze_backbone_bn: bool = False,
):
    """Run one training stage and persist the best validation checkpoint."""
    for epoch in range(epochs):
        train_loss, train_acc = train_one_epoch(
            model=model,
            dataloader=train_loader,
            criterion=criterion,
            optimizer=optimizer,
            device=device,
            scaler=scaler,
            freeze_backbone_bn=freeze_backbone_bn,
        )
        val_loss, val_acc = validate_one_epoch(
            model=model,
            dataloader=val_loader,
            criterion=criterion,
            device=device,
        )
        scheduler.step()

        print(
            f"[{stage_name}] "
            f"Epoch {epoch + 1:02d}/{epochs:02d} | "
            f"Train Loss: {train_loss:.4f} | "
            f"Train Acc: {train_acc:.2%} | "
            f"Val Loss: {val_loss:.4f} | "
            f"Val Acc: {val_acc:.2%}"
        )

        if val_acc > best_val_accuracy:
            best_val_accuracy = val_acc
            save_training_checkpoint(
                path=checkpoint_path,
                model=model,
                optimizer=optimizer,
                scheduler=scheduler,
                epoch=epoch,
                stage=stage_name,
                val_accuracy=val_acc,
                val_loss=val_loss,
            )
            print()
            print(f"  -> Novo melhor modelo salvo ({val_acc:.2%})")
            print()

    return best_val_accuracy
