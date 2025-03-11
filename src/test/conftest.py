from pytest import fixture
import uuid

URL = "https://jsonplaceholder.typicode.com/todos/1"
BACKEND = "http://127.0.0.1:8003"
TIMEOUT_URL = "http://httpbin.org/delay/5"
UNAUTHORIZED_URL = "http://httpbin.org/status/401"


@fixture
def url():
    return URL


@fixture
def token():
    return str(uuid.uuid4())


@fixture
def backend_url():
    return BACKEND


@fixture
def timeout_url():
    return TIMEOUT_URL


@fixture
def unauthorized_url():
    return UNAUTHORIZED_URL
