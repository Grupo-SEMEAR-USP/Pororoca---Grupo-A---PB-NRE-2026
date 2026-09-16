# Arquitetura de software

## Visão geral

O Wallyngton é organizado como um workspace ROS 2 com pacotes independentes por domínio. Tópicos, serviços, ações e interfaces próprias serão utilizados para evitar acoplamento direto entre subsistemas.

A arquitetura ainda está em construção. Este documento distingue componentes existentes de módulos planejados.

## Componentes existentes

### `wallington_interfaces`

Centraliza interfaces compartilhadas. Atualmente contém:

```text
msg/AudioOutput.msg
```

A mensagem possui os campos:

```text
string text_to_speech
string audio_path
```

### `voice_interaction`

Contém os experimentos iniciais de síntese de fala:

- `voice_synthesizer`: recebe `AudioOutput`, sintetiza texto com Piper e reproduz o áudio;
- `text_emmiter`: publica periodicamente uma mensagem de texto em um tópico de teste;
- `voice_model/`: modelo ONNX e configuração da voz.

Os nós ainda utilizam mensagens e tópicos diferentes e não formam um pipeline conectado.

### `plant_vision`

Reúne a implementação atual de visão computacional em camadas reutilizáveis:

```text
plant_vision/
├── data/          # Dataset Flowers102, transforms e dataloaders
├── models/        # Arquitetura MobileNetV3 Small
├── training/      # Loops de treinamento e checkpoints
├── inference/     # Carregamento e predição
├── evaluation/    # Métricas e visualizações
├── vision/        # Detecção geométrica com OpenCV
└── cli/           # Aplicações executáveis
```

O pacote oferece executáveis para treinamento, avaliação, inferência em imagem, classificação por câmera e detecção de marcadores amarelos. Ele ainda não publica nem consome tópicos ROS 2; essa fronteira será definida quando os contratos com navegação e manipulação forem conhecidos.

Datasets, checkpoints e resultados permanecem fora do Git. Por padrão, o pacote procura esses artefatos na raiz do workspace, podendo usar caminhos externos pelas variáveis:

- `WALLYNGTON_WORKSPACE_ROOT`;
- `WALLYNGTON_VISION_DATA_DIR`;
- `WALLYNGTON_VISION_MODELS_DIR`;
- `WALLYNGTON_VISION_RESULTS_DIR`;
- `WALLYNGTON_VISION_CHECKPOINT`.

## Domínios planejados

```text
src/
├── wallington_interfaces/     # Existente: interfaces compartilhadas
├── voice_interaction/         # Existente: síntese de fala
├── plant_vision/              # Existente: classificação e percepção visual
├── speech_recognition/        # Planejado: escuta e transcrição
├── navigation/                # Planejado: localização e navegação
├── manipulation/              # Planejado: coordenação da garra
└── robot_bringup/             # Planejado: launch e configuração integrada
```

Diretórios planejados só devem ser criados quando houver código ou configuração real para eles.

## Fluxos de alto nível

### Interação vocal

```text
microfone → reconhecimento de fala → interpretação/comando
                                      ↓
                              síntese de fala → alto-falante
```

### Visão computacional

```text
câmera → aquisição de imagem → classificação de plantas
                              → detecção de marcadores
                              → futura publicação ROS 2
```

### Navegação

```text
sensores → localização/percepção → planejamento → comandos de movimento
```

### Manipulação

```text
comando de tarefa → planejamento da ação → interface com garra/firmware
```

## Princípios para evolução

1. Cada pacote deve possuir uma responsabilidade principal clara.
2. Interfaces compartilhadas devem permanecer em `wallington_interfaces`.
3. Hardware, modelos e caminhos locais devem ser parametrizáveis.
4. Nós devem se integrar por contratos explícitos, evitando dependências diretas desnecessárias.
5. Launch files e configurações integradas devem ficar em um pacote de `bringup` quando esse fluxo existir.
6. Modelos de ML devem ter versão, origem e checksum sem crescer indefinidamente no histórico Git.
7. Mudanças de interface devem ser coordenadas entre produtores e consumidores.
8. A plataforma embarcada deve ser definida antes de fixar a estratégia final de inferência e aceleração.

## Limites do repositório

O workspace cobre o software de alto nível do robô. Projetos mecânicos, eletrônicos e firmware podem possuir artefatos ou repositórios próprios; a integração deve ocorrer por interfaces documentadas.
