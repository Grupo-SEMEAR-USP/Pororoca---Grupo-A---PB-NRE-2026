# `plant_vision`

Pacote ROS 2 em Python para o subsistema de visão computacional do Wallyngton.

A implementação atual reúne classificação de espécies do Oxford Flowers 102, treinamento e avaliação com MobileNetV3 Small, inferência em imagens e webcam e detecção de marcadores amarelos com OpenCV.

Dependências Python são gerenciadas pelo grupo `vision` do `pyproject.toml` na raiz do workspace. Datasets, checkpoints e resultados permanecem fora do Git.

Consulte o [`README.md`](../../README.md) do projeto e [`docs/DEVELOPMENT.md`](../../docs/DEVELOPMENT.md) para preparação e execução.
