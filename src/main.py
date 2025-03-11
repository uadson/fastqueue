"""
API desenvolvida com FastAPI para gerenciar requisições assíncronas utilizando Celery.

Rotas disponíveis:
    - 'POST /request/' -> Enfileira uma nova requisição para a API externa.
    - 'GET' /status/{task_id}' -> Retorna o status da tarefa enfileirada.
"""

from fastapi import FastAPI

from celery_worker import fetch_data

# Inicializa a aplicação FastAPI
app = FastAPI()


@app.post('/request/')
def send_request(url: str, token: str):
    """
    Enfileira uma requisição para uma API externa.

    Args:
        url (str): URL da API externa a ser acessada.
        token (str): Token de autenticação (Bearer Token).

        Returns:
            dict: ID da tarefa Celery e status inicial.
    """

    headers = {'Authorization': f'Bearer {token}'}
    task = fetch_data.apply_async(args=[url], kwargs={'headers': headers})
    return {'task_id': task.id, 'status': task.status}


@app.get('/status/{task_id}')
def get_task_status(task_id: str):
    """
    Retorna o status da tarefa enfileirada.

    Args:
        task_id(str): ID da tarefa Celery.

    Returns:
        dict: Status da tarefa e resultado, se disponível.
    """

    task_result = fetch_data.AsyncResult(task_id)
    return {
        'task_id': task_id,
        'status': task_result.status,
        'result': task_result.result if task_result.ready() else None,
    }
