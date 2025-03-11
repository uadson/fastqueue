# Testes unitários para a função Celery.
import httpx

from celery_worker import fetch_data

import pytest


def test_fetch_data_response(url):
    """
    Testa a função Celery simulando uma API externa.
    """
    fake_response = {
        "userId": 1,
        "id": 1,
        "title": "delectus aut autem",
        "completed": False,
    }

    with httpx.Client() as client:
        response = client.get(url)
        assert response.status_code == httpx.codes.OK
        result = fetch_data(url)
        assert result == fake_response


def test_fetch_data_timeout(timeout_url):
    """
    Testa o comportamento da função Celery quando ocorre um timeout.
    """
    with pytest.raises(Exception, match="Timeout ao acessar API externa"):
        fetch_data(timeout_url)


def test_fetch_data_unauthorized(unauthorized_url):
    """
    Testa o comportamento da função Celery quando ocorre um
    erro de autenticação
    """
    with pytest.raises(
        Exception, match="Falha na autenticação, verifique suas credenciais"
    ):
        fetch_data(unauthorized_url)
