import uuid

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    """
    Retorna uma instancia do TestClient
    """
    return TestClient(app)


@pytest.fixture
def url():
    """
    Retorna a URL de teste
    """
    return "http://example.com/api"


@pytest.fixture
def token():
    """
    Retorna um token de teste
    """
    return str(uuid.uuid4())


@pytest.fixture
def mock_url_and_headers():
    """
    Retorna uma url e um header para teste
    """
    token = str(uuid.uuid4())
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

    return {"url": "http://example.com/api", "headers": headers}


@pytest.fixture
def mock_url_and_invalid_headers():
    """
    Retorna uma url e um header inválidos para teste
    """
    token = "invalid_token"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    return {"url": "http://example.com/api", "headers": headers}
