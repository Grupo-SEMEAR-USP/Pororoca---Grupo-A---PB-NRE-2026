"""Training checkpoint persistence."""

from pathlib import Path

import torch


def save_training_checkpoint(
    path: str | Path,
    model,
    optimizer,
    scheduler,
    epoch: int,
    stage: str,
    val_accuracy: float,
    val_loss: float,
) -> None:
    """Save the same training state used by the original pipeline."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "scheduler_state_dict": scheduler.state_dict(),
            "epoch": epoch,
            "stage": stage,
            "val_accuracy": val_accuracy,
            "val_loss": val_loss,
        },
        path,
    )
