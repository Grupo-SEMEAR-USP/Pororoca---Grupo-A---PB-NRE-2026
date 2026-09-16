# Problemas e pendências conhecidas

Este documento registra limitações técnicas e decisões ainda abertas no estado atual do projeto.

## Integração dos nós de voz

- `text_emmiter` publica `example_interfaces/String` no tópico `fala_wally`.
- `voice_synthesizer` assina `wallington_interfaces/AudioOutput` no tópico `voice_output`.
- Portanto, os dois nós atuais não se comunicam diretamente.

É necessário decidir qual mensagem e qual tópico representarão o contrato oficial do fluxo de síntese.

## Integração da visão com ROS 2

O pacote `plant_vision` oferece biblioteca e aplicações executáveis, mas ainda não publica nem consome tópicos ROS 2. A interface só deverá ser fixada depois de definir:

- quais resultados serão consumidos por navegação e manipulação;
- se imagens serão recebidas por tópico ou diretamente da câmera;
- frequência, latência e hardware de inferência;
- mensagens, serviços ou ações necessários.

## Modelo de classificação

O checkpoint local `models/best_model.pt` não é versionado. Antes de distribuí-lo ao grupo, é necessário definir:

- armazenamento por Git LFS, release ou serviço externo;
- versão e checksum do artefato;
- hardware de destino e formato de inferência;
- procedimento reproduzível de download ou exportação.

O código utiliza atualmente PyTorch com CUDA 12.6 no ambiente de desenvolvimento x86-64. Essa escolha não determina a implantação final no computador embarcado.

## Metadados e licença

`voice_interaction` e `wallington_interfaces` ainda possuem metadados provisórios, incluindo versão, descrição e licença. `plant_vision` possui descrição e versão próprias, mas mantém a licença pendente pela mesma razão.

A licença do projeto não deve ser escolhida sem decisão do grupo ou da instituição.

## Arquivo `requirements.txt`

O arquivo foi preservado como registro legado do ambiente original. Ele inclui pacotes do ROS 2, ferramentas, exemplos e versões do ambiente dos autores.

Ele não é mais a fonte de verdade. Dependências Python diretas ficam em `pyproject.toml`, e a resolução exata fica em `uv.lock`.

## Nomes e convenções

- O robô é referido como **Wallyngton**, enquanto o pacote existente usa `wallington_interfaces`.
- O identificador `text_emmiter` utiliza uma grafia não convencional de “emitter”.
- O código de voz ainda possui estilo experimental e pouco uniforme.

Esses nomes foram preservados porque alterações afetariam comandos, imports ou interfaces conhecidas pelos autores.

## Shebangs e caminhos locais da voz

Os scripts de voz possuem shebangs associados a caminhos locais específicos e com uso de `~`. A execução por `ros2 run` reduz parte do impacto, mas os cabeçalhos deverão ser revistos no futuro.

## Modelo de voz no Git

O modelo `wendel.onnx` possui aproximadamente 61 MB e continua versionado diretamente. Antes de adicionar novos modelos, o grupo deve definir uma política comum para artefatos grandes.

## Comportamento do sintetizador

- o modelo de voz é carregado durante a importação do módulo;
- uma nova stream de áudio é aberta para cada callback;
- o campo `audio_path` ainda não é utilizado;
- não há tratamento explícito de falhas do dispositivo de áudio ou da síntese.

## Verificação automatizada

O repositório ainda não possui uma suíte funcional automatizada nem integração contínua. Os arquivos de teste existentes em `voice_interaction` são os linters gerados pelo template ROS 2 e não cobrem o comportamento dos nós.

Neste estágio, a validação é feita por build, análise estática, smoke tests e execução manual dos fluxos de hardware relevantes.

## Bringup e integração geral

Ainda não existem:

- launch files para iniciar o sistema;
- pacote de `bringup`;
- parâmetros ROS externos;
- integração entre voz, visão, navegação e manipulação;
- documentação de hardware e tópicos do sistema completo.

Esses componentes deverão ser implementados conforme os contratos entre subsistemas forem definidos.
