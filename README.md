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
python -m src.broker.server
```

### 2. Iniciar Subscribers (múltiplos terminais)

```bash
python -m src.subscriber.client
```

### 3. Publicar Atualização

```bash
python -m src.publisher.client
```

## Demonstração

Execute múltiplos subscribers e depois o publisher. Todos os subscribers receberão as atualizações simultaneamente, demonstrando o paradigma Pub/Sub sem polling.

## TODO

- [ ] Implementar Broker (src/broker/server.py)
- [ ] Implementar Publisher (src/publisher/client.py)
- [ ] Implementar Subscriber (src/subscriber/client.py)
- [ ] Testar integração
