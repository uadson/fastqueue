from pytest import fixture
import uuid

URL = "https://jsonplaceholder.typicode.com/todos/1"
BACKEND = "http://localhost"
TIMEOUT_URL = "http://httpbin.org/delay/5"
UNAUTHORIZED_URL = "http://httpbin.org/status/401"


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
def backend_url():
    """
    Retorna a URL do backend
    """
    return BACKEND


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
