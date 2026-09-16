# Ambiente de desenvolvimento

## Plataforma de referência

O workspace adota:

- Ubuntu 24.04 LTS;
- ROS 2 Jazzy;
- Python 3.12.x;
- `rosdep` para dependências ROS e de sistema;
- `uv` para dependências Python;
- `colcon` para build do workspace.

A arquitetura do computador embarcado ainda não foi definida. A distribuição final de PyTorch e dos modelos deverá ser revista quando o hardware for escolhido.

## Responsabilidade das ferramentas

- `package.xml`: dependências diretas de cada pacote ROS 2;
- `rosdep`: tradução dessas dependências para a plataforma;
- `pyproject.toml`: dependências Python diretas e grupos do workspace;
- `uv.lock`: resolução exata e reproduzível;
- `requirements.txt`: snapshot legado, não utilizado como fonte de verdade;
- `colcon`: build e instalação dos pacotes ROS 2.

## Grupos Python

### `voice`

- Piper TTS;
- `sounddevice`.

### `vision`

- pacote local `plant_vision`;
- NumPy e Pillow;
- PyTorch e Torchvision com CUDA 12.6;
- OpenCV;
- Matplotlib;
- scikit-learn.

O grupo é opcional devido ao tamanho das dependências de aprendizado profundo.

### `dev`

- Colcon e extensões de build para ROS 2;
- Ruff.

Os grupos `voice` e `dev` são instalados por padrão. O grupo `vision` é ativado pelos desenvolvedores que trabalham com percepção visual.

## Preparação do workspace

```bash
git clone https://github.com/Grupo-SEMEAR-USP/Pororoca---Grupo-A---PB-NRE-2026.git
cd Pororoca---Grupo-A---PB-NRE-2026
source /opt/ros/jazzy/setup.bash
```

Instale dependências ROS e de sistema:

```bash
rosdep update
rosdep install \
    --from-paths src \
    --ignore-src \
    --rosdistro jazzy \
    --skip-keys="python-piper-tts-pip python3-sounddevice-pip python3-numpy python3-opencv python3-pil python3-matplotlib python3-sklearn python3-torch python3-torchvision" \
    -r -y
```

As chaves ignoradas são gerenciadas e versionadas pelo `uv`; continuam no `package.xml` para manter os pacotes autodescritivos.

Crie o ambiente com acesso aos módulos Python fornecidos pelo ROS:

```bash
uv venv --python /usr/bin/python3.12 --system-site-packages
uv sync
source .venv/bin/activate
```

Para desenvolver visão:

```bash
uv sync --group vision
```

Para instalar todos os grupos:

```bash
uv sync --all-groups
```

Não use `pip install -r requirements.txt` no fluxo normal.

## Build

```bash
colcon build --symlink-install
source install/setup.bash
```

O `colcon` instalado no grupo `dev` deve ser o primeiro encontrado no `PATH` após a ativação da `.venv`. Assim, os executáveis Python gerados pelo build usam o mesmo interpretador que contém as dependências dos grupos `voice` e `vision`.

Em cada terminal novo:

```bash
source /opt/ros/jazzy/setup.bash
source .venv/bin/activate
source install/setup.bash
```

## Execução

### Voz

```bash
ros2 run voice_interaction voice_synthesizer
ros2 run voice_interaction text_emmiter
```

### Visão

O checkpoint padrão deve estar em `models/best_model.pt`. Esse diretório é local e ignorado pelo Git.

```bash
ros2 run plant_vision predict_plant /caminho/para/imagem.jpg
ros2 run plant_vision classify_camera
ros2 run plant_vision detect_tag_camera
ros2 run plant_vision evaluate_classifier
ros2 run plant_vision train_classifier
```

Ferramentas de inspeção podem ser chamadas a partir da raiz:

```bash
python src/plant_vision/scripts/smoke_test_model.py
python src/plant_vision/scripts/inspect_dataloader.py
```

### Webcam no Windows

O WSL não expõe a webcam como um dispositivo OpenCV comum. Para câmera local, execute o pacote em um ambiente Python 3.12 nativo do Windows e aponte o `uv` para este projeto. Dados e checkpoint podem continuar no workspace WSL por um caminho UNC ou ser configurados pelas variáveis `WALLYNGTON_VISION_*`.

## Configuração dos artefatos de visão

Em uma cópia-fonte do workspace, os valores padrão são:

```text
data/                  dataset local
models/best_model.pt   checkpoint local
results/               relatórios e figuras
```

Em uma instalação que não preserve a árvore-fonte, o fallback é determinístico: `%LOCALAPPDATA%/Wallyngton` no Windows e `${XDG_DATA_HOME:-~/.local/share}/wallyngton` no Linux. O diretório atual do processo não altera esses caminhos.

Caminhos alternativos:

```bash
export WALLYNGTON_VISION_DATA_DIR=/caminho/dados
export WALLYNGTON_VISION_CHECKPOINT=/caminho/modelo.pt
export WALLYNGTON_VISION_RESULTS_DIR=/caminho/resultados
```

`WALLYNGTON_WORKSPACE_ROOT` pode substituir de uma vez a raiz usada pelos três diretórios padrão.

## Dependências

```bash
uv add --group voice <pacote>
uv add --group vision <pacote>
uv add --group dev <pacote>
uv lock --check
```

Dependências ROS ou de sistema também devem ser declaradas no `package.xml` correspondente com chaves válidas do `rosdep`.

## Verificações locais

```bash
uv lock --check
ruff check src/plant_vision
python -m compileall -q src
python src/plant_vision/scripts/smoke_test_model.py
```

Pacotes que dependem de câmera, áudio, GPU ou do ROS devem informar claramente quais verificações de hardware foram realizadas.

## Limpeza do build

```bash
rm -rf build install log
colcon build --symlink-install
```

`build/`, `install/` e `log/` são artefatos locais e não devem ser versionados.
