# Wallyngton — Grupo A — Projeto de Bixo NRE 2026

Repositório da frente de programação do **Grupo A** no ciclo **Projeto de Bixo 2026** do **Núcleo de Robótica para Extensão (NRE)**, pertencente ao grupo SEMEAR.

O ciclo tem finalidade didática e introduz os membros ingressantes ao desenvolvimento de sistemas robóticos. O robô do grupo é o **Wallyngton**, inspirado no personagem WALL-E.

> O projeto está em desenvolvimento. Os pacotes atuais representam subsistemas funcionais e experimentais que ainda serão conectados por interfaces ROS 2.

## Objetivos de software

A arquitetura deverá apoiar progressivamente:

- navegação autônoma;
- interação vocal por escuta e síntese de fala;
- reconhecimento de espécies de plantas e percepção visual;
- integração com a garra e demais mecanismos físicos;
- coordenação dos subsistemas por ROS 2.

Este repositório concentra o software de alto nível. Mecânica, elétrica e firmware são desenvolvidos pelas respectivas frentes do grupo.

## Componentes atuais

### `wallington_interfaces`

Pacote de interfaces compartilhadas. Atualmente define `AudioOutput`, mensagem com campos para o texto a ser sintetizado e o caminho de um arquivo de áudio.

### `voice_interaction`

Pacote Python com os primeiros experimentos de síntese de fala:

- emissor de texto para testes;
- sintetizador baseado em Piper TTS;
- reprodução de áudio com `sounddevice`;
- modelo de voz em português armazenado no pacote.

### `plant_vision`

Pacote Python para o subsistema de visão computacional:

- classificação das 102 categorias do dataset Oxford Flowers 102;
- treinamento e fine-tuning de MobileNetV3 Small;
- avaliação, métricas e visualizações;
- inferência em imagens e webcam;
- detecção geométrica de marcadores amarelos com OpenCV.

As aplicações de visão já podem ser executadas de forma independente. Sua exposição como nós e interfaces ROS 2 permanece como trabalho de integração futura.

## Estrutura do repositório

```text
Pororoca---Grupo-A---PB-NRE-2026/
├── src/
│   ├── wallington_interfaces/        # Mensagens, serviços e ações compartilhados
│   ├── voice_interaction/            # Síntese de fala
│   └── plant_vision/                 # Classificação e percepção visual
│       ├── plant_vision/             # Biblioteca e aplicações Python
│       ├── scripts/                  # Ferramentas de inspeção e smoke tests
│       ├── package.xml
│       ├── setup.cfg
│       └── setup.py
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DEVELOPMENT.md
│   └── KNOWN_ISSUES.md
├── CONTRIBUTING.md
├── pyproject.toml                    # Dependências Python diretas e grupos
├── uv.lock                           # Resolução reproduzível das dependências
├── .python-version                   # Python 3.12
├── requirements.txt                  # Snapshot legado do ambiente original
└── README.md
```

Dados, checkpoints e resultados são locais e não são versionados:

```text
data/
models/
results/
```

## Plataforma de referência

- Ubuntu 24.04 LTS;
- ROS 2 Jazzy;
- Python 3.12.x;
- `rosdep` para dependências ROS e de sistema;
- `uv` para dependências Python;
- `colcon` executado pelo ambiente virtual para build do workspace.

## Preparação rápida

```bash
git clone https://github.com/Grupo-SEMEAR-USP/Pororoca---Grupo-A---PB-NRE-2026.git
cd Pororoca---Grupo-A---PB-NRE-2026

source /opt/ros/jazzy/setup.bash

uv venv --python /usr/bin/python3.12 --system-site-packages
uv sync
source .venv/bin/activate

colcon build --symlink-install
source install/setup.bash
```

O grupo de visão é opcional porque inclui PyTorch e CUDA e ocupa vários gigabytes:

```bash
uv sync --group vision
```

Consulte [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md) para o fluxo completo com `rosdep`, grupos de dependência e configuração dos artefatos de visão.

## Execução

### Voz

```bash
ros2 run voice_interaction voice_synthesizer
ros2 run voice_interaction text_emmiter
```

Os dois nós ainda não formam um pipeline conectado; a diferença entre suas interfaces está registrada em [`docs/KNOWN_ISSUES.md`](docs/KNOWN_ISSUES.md).

### Visão

Depois de instalar o grupo `vision` e compilar o workspace:

```bash
ros2 run plant_vision predict_plant /caminho/para/imagem.jpg
ros2 run plant_vision classify_camera
ros2 run plant_vision detect_tag_camera
ros2 run plant_vision evaluate_classifier
```

O classificador espera um checkpoint local em:

```text
models/best_model.pt
```

O arquivo não acompanha o repositório. A política definitiva de distribuição de modelos ainda será decidida pelo grupo.

## Documentação

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md): componentes existentes e direção arquitetural;
- [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md): ambiente, dependências, build e execução;
- [`docs/KNOWN_ISSUES.md`](docs/KNOWN_ISSUES.md): limitações e decisões pendentes;
- [`CONTRIBUTING.md`](CONTRIBUTING.md): convenções de colaboração.
