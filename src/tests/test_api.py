# Testes para a API do projeto.
import httpx


def test_send_request(url, token, backend_url):
    """
    Testa se a API enfileira corretamente uma nova requisição.
    """
    with httpx.Client(base_url=backend_url) as client:
        response = client.post(
            f"/request/?url={url}&token={token}",
        )

        assert response.status_code == httpx.codes.OK
        assert "task_id" in response.json()
        assert response.json()["status"] == "PENDING"


def test_get_task_status(backend_url):
    """
    Testa a rota que retorna o status de uma tarefa.
    """
    with httpx.Client(base_url=backend_url) as client:
        response = client.get(f"/status/test_task_id")
        assert response.status_code == httpx.codes.OK
        assert "task_id" in response.json()
        assert "status" in response.json()
