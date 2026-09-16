# Contribuindo

Estas convenções iniciais existem para manter o workspace compreensível enquanto novos membros e módulos são adicionados.

## Fluxo recomendado

1. Atualize sua cópia local da branch principal.
2. Crie uma branch curta para a tarefa.
3. Faça commits pequenos e com responsabilidade clara.
4. Compile apenas os pacotes afetados durante o desenvolvimento.
5. Antes de solicitar integração, descreva o que mudou e como validar.

Exemplo:

```bash
git switch -c feature/nome-da-funcionalidade
```

## Organização

- Pacotes ROS 2 ficam diretamente em `src/`.
- Cada pacote deve ter uma responsabilidade principal.
- Interfaces compartilhadas ficam em `wallington_interfaces`.
- Não crie pastas vazias para funcionalidades ainda não implementadas.
- Documentação geral fica em `docs/`.
- Arquivos gerados por build não devem ser versionados.

## Dependências

- Dependências ROS e de sistema devem ser declaradas no `package.xml` do pacote que as utiliza.
- Dependências Python da interação vocal devem ser adicionadas ao grupo `voice` com `uv add --group voice <pacote>`.
- Dependências Python de visão devem ser adicionadas ao grupo `vision` com `uv add --group vision <pacote>`.
- Ferramentas de desenvolvimento devem ser adicionadas ao grupo `dev` com `uv add --group dev <pacote>`.
- Dependências transitivas pertencem ao `uv.lock` e não devem ser copiadas manualmente para `pyproject.toml`.
- O `requirements.txt` atual é legado e não deve receber novas alterações manuais.

Depois de modificar dependências, valide o lockfile:

```bash
uv lock --check
```

## Antes de enviar mudanças

```bash
source /opt/ros/jazzy/setup.bash
uv sync --all-groups
ruff check src/plant_vision
python -m compileall -q src
colcon build --symlink-install
source install/setup.bash
```

Quando um pacote não puder ser validado completamente por depender de hardware, informe claramente:

- qual hardware é necessário;
- quais passos foram executados;
- o que permaneceu sem teste.

## Interfaces ROS 2

Mudanças em mensagens, serviços, ações, nomes de tópicos ou parâmetros afetam outros módulos. Antes de alterá-los:

1. identifique consumidores e produtores;
2. comunique a mudança ao grupo;
3. atualize a documentação;
4. valide novamente os pacotes dependentes.

## Commits

Prefira mensagens objetivas, por exemplo:

```text
feat(voice): adiciona nó de reconhecimento de fala
fix(navigation): corrige parâmetro do mapa
refactor(interfaces): reorganiza mensagens de áudio
docs: documenta preparação do workspace
```

Evite commits que misturem reorganização, funcionalidade e formatação sem necessidade.

## Artefatos grandes

Não adicione novos modelos, datasets, áudios extensos ou arquivos binários grandes antes de definir onde esses artefatos serão armazenados. Registre versão, origem e checksum quando forem externos ao Git.
