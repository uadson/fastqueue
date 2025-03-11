from pytest import fixture
import uuid
from fastapi.testclient import TestClient
from src.main import app

URL = "https://jsonplaceholder.typicode.com/todos/1"
TIMEOUT_URL = "http://httpbin.org/delay/5"
UNAUTHORIZED_URL = "http://httpbin.org/status/401"


@fixture
def client():
    """
    Retorna uma instancia do TestClient
    """
    return TestClient(app)


@fixture
def url():
    """
    Retorna a URL de teste
    """
    return URL


@fixture
def token():
    """
    Retorna um token de teste
    """
    return str(uuid.uuid4())


@fixture
def timeout_url():
    """
    Retorna uma URL com timeout
    """
    return TIMEOUT_URL


@fixture
def unauthorized_url():
    """
    Retorna uma URL com status 401
    """
    return UNAUTHORIZED_URL
