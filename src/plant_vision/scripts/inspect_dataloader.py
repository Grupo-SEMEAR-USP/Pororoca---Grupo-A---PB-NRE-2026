"""Inspect one batch from the training dataloader."""

from plant_vision.data import create_dataloaders


def main():
    train_loader, _, _ = create_dataloaders(batch_size=32)
    images, labels = next(iter(train_loader))

    print("Shape das imagens:", images.shape)
    print("Shape dos labels:", labels.shape)
    print()
    print("Tipo das imagens:", images.dtype)
    print("Tipo dos labels:", labels.dtype)
    print()
    print("Primeiros labels:")
    print(labels[:10])


if __name__ == "__main__":
    main()
