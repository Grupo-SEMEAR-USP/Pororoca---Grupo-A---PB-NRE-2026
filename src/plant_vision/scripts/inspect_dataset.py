"""Inspect basic Flowers102 dataset information."""

import random

import matplotlib.pyplot as plt
from plant_vision.config import DATA_DIR
from torchvision.datasets import Flowers102


def main():
    train_dataset = Flowers102(root=DATA_DIR, split="train", download=True)
    val_dataset = Flowers102(root=DATA_DIR, split="val", download=True)
    test_dataset = Flowers102(root=DATA_DIR, split="test", download=True)

    print("Quantidade de imagens:")
    print("Train:", len(train_dataset))
    print("Validation:", len(val_dataset))
    print("Test:", len(test_dataset))

    image, label = train_dataset[0]
    print()
    print(" ==== Info Example Image ====")
    print("Tipo da imagem:", type(image))
    print("Tamanho da imagem:", image.size)
    print("Label:", label)
    print()

    _, axes = plt.subplots(2, 4, figsize=(12, 7))
    for axis in axes.flat:
        index = random.randrange(len(train_dataset))
        image, label = train_dataset[index]
        axis.imshow(image)
        axis.set_title(f"Classe: {label}")
        axis.axis("off")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
