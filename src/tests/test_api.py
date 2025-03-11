# Testes para a API do projeto.
from fastapi import status


def test_send_request(url, token, client):
    """
    Testa se a API enfileira corretamente uma nova requisição.
    """
    response = client.post(
        f"/request/?url={url}&token={token}",
    )

    assert response.status_code == status.HTTP_200_OK
    assert "task_id" in response.json()
    assert response.json()["status"] == "PENDING"


def test_get_task_status(client):
    """
    Testa a rota que retorna o status de uma tarefa.
    """
    response = client.get(f"/status/test_task_id")
    assert response.status_code == status.HTTP_200_OK
    assert "task_id" in response.json()
    assert "status" in response.json()
