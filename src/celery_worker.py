"""
Módulo responsável pelo processamento assíncrono de tarefas utilizando Celery.

- O Celery é configurado para utilizar o RabbitMQ como broker.
- A função 'fetch_data' realiza uma requisição HTTP assíncrona.
- Implementa tratamento de erros para timeout e autenticação.
"""

import requests
from celery import Celery

"""
Brokers são 'mensageiros' intermidiários que permitem a comunicação assíncrona entre
diferentes partes de um sistema. Eles atuam como fila de mensagens, garantindo que os
dados sejam entregues corretamente entre um produtor (worker) e um consumidor (task).

No contexto do Celery, o Broker(RabbitMQ) recebe as tarefas da aplicação e as distribui para
os produtores(workers) que irão processá-las.
"""

# Configuração do Celery com RabbitMQ como Broker
celery_app = Celery(
    'tasks',
    broker='pyamqp://guest@localhost//',  # URL de conexão com o RabbitMQ
    backend='rpc://',  # URL de conexão com o backend - armaezana os resultados das tarefas
)


@celery_app.task(
    bind=True,
    autoretry_for=(requests.exceptions.RequestException,),
    retry_backoff=True,
    max_retries=3,
)
def fetch_data(self, url: str, headers: dict = None):
    """
    Realiza uma requisição GET para uma API externa, com tolerância a falhas.

    Args:
        url (str): URL da API externa.
        headers (dict, opcional): Dicionário com cabeçalhos HTTP, incluindo autenticação.

    Returns:
        dict: Resposta JSON da API externa ou mensagem de erro.

    Tratamento de Erros:
        - Timeout -> Reexecuta a tarefa automaticamente até 3 vezes.
        - HTTP 401 (não autorizado) -> Retorna erro sem reexecutar a tarefa.
    """

    try:
        response = requests.get(url, headers=headers, timeout=5)
        UNAUTHORIZED = 401
        if response.status_code == UNAUTHORIZED:
            raise Exception('Falha na autenticação, verifique suas credenciais')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        raise self.retry(exc=Exception('Timeout ao acessar API externa'))
    except requests.exceptions.HTTPError as err:
        raise self.retry(exc=err)
