# Pub/Sub Placar de Futebol em Tempo Real

Sistema demonstrando o paradigma Publisher/Subscriber com Broker gRPC customizado para a disciplina de Sistemas Distribuídos do curso de Ciência da Computação da UFF.

## Arquitetura

```
[Publisher] → (gRPC Unary) → [Broker] → (gRPC Streaming) → [Subscribers]
```

## Pré-requisitos

- Python 3.12+
- uv (gerenciador de pacotes)

## Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/futebol-pubsub.git
cd futebol-pubsub

# Instale as dependências
uv sync
```

## Execução

### 1. Iniciar o Broker

```bash
source .venv/bin/activate

python -m src.broker.server
```

### 2. Iniciar Subscribers (múltiplos terminais)

```bash
source .venv/bin/activate

python -m src.subscriber.subscriber
```

### 3. Publicar Atualização

```bash
source .venv/bin/activate

python -m src.publisher.publisher
```

## Demonstração

Execute múltiplos subscribers e depois o publisher. Todos os subscribers receberão as atualizações simultaneamente, demonstrando o paradigma Pub/Sub sem polling.

## Filtro por Time

O subscriber pode escolher receber atualizações de todos os jogos ou apenas de um time específico. Ao iniciar, digite o nome do time para filtrar ou deixe vazio para receber todas as atualizações.

## TODO

- [X] Implementar Broker (src/broker/server.py)
- [X] Implementar Publisher (src/publisher/publisher.py)
- [X] Implementar Subscriber (src/subscriber/subscriber.py)
- [X] Testar integração
- [X] Adicionar filtros por time
