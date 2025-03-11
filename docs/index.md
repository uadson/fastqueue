# Bem vindo (a) documentação do FastQueue

## FastAPI + Celery + RabbitMQ: Processamento Assíncrono de APIs Externas

Este projeto demonstra como utilizar **FastAPI** e **Celery** com **RabbitMQ** para realizar chamadas assíncronas a APIs externas, lidando com falhas como timeout e autenticação.

## 📌 Tecnologias Utilizadas
- **FastAPI** → Framework para criar a API.
- **Celery** → Gerenciamento de tarefas assíncronas.
- **RabbitMQ** → Broker de mensagens.
- **Flower** → Monitoramento das tarefas Celery.
- **Requests** → Biblioteca para chamadas HTTP.

---

## 🚀 Como Rodar o Projeto

### 1️⃣ Instalar Dependências
```bash
pip install fastapi celery[redis] uvicorn requests flower
```

### 2️⃣ Iniciar o RabbitMQ

```bash
docker run -d --hostname rmq-broker --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
```
* Acessar o painel RabbitMQ em: http://localhost:15672
* Usuário/Senha padrão: guest/guest

### 3️⃣ Iniciar o Celery Worker

```bash
celery -A celery_worker.celery_app worker --loglevel=info
```

### 4️⃣ Rodar FastAPI
```bash
fastapi dev
```

## Monitoramento com Flower

O **Flower** permite visualizar e monitorar as tarefas do Celery em tempo real. 


### 1️⃣ Iniciar o Flower
```bash
celery -A celery_worker.celery_app flower --port=5555
```

### 2️⃣ Acessar o Painel do Flower
* Acessar http://localhost:5555 para visualizar as tarefas em tempo real.
* Lá você pode ver: ✅ Tarefas pendentes, em execução e finalizadas.
✅ Tempo de execução e falhas.
✅ Tentativas de reexecução por timeout ou erro.


## Testando a API

* Enviar uma requisição para a API externa
```bash
curl -X 'POST' 'http://127.0.0.1:8000/request/' -H 'Content-Type: application/json' -d '{"url": "https://jsonplaceholder.typicode.com/todos/1", "token": "meu_token"}'
```

* Resposta esperada:
```JSON
{
    "task_id": "b95b9e8f-2f27-49b1-97b5-34aef06b745d",
    "status": "PENDING"
}
```

## Consultar o Status da Tarefa
```bash
curl -X 'GET' 'http://127.0.0.1:8000/status/b95b9e8f-2f27-49b1-97b5-34aef06b745d'
```

* Resposta enquanto está processando:
```JSON
{
    "task_id": "b95b9e8f-2f27-49b1-97b5-34aef06b745d",
    "status": "PENDING",
    "result": null
}
```

* Resposta após concluir:
```JSON
{
    "task_id": "b95b9e8f-2f27-49b1-97b5-34aef06b745d",
    "status": "SUCCESS",
    "result": {
        "userId": 1,
        "id": 1,
        "title": "delectus aut autem",
        "completed": false
    }
}
```

## Como funciona?

    1 - O FastAPI recebe uma requisição para acessar uma API externa.
    2 - A requisição é enviada para a fila do RabbitMQ usando Celery.
    3 - O Worker Celery recupera a tarefa e faz a requisição à API externa.
    4 - Se houver timeout ou erro, o Celery tenta novamente automaticamente.
    5 - O usuário pode consultar o status da tarefa via API.
