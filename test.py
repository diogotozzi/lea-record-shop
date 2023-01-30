import pytest
from sanic import Sanic, response


@pytest.fixture
def app():
    sanic_app = Sanic("LeaRecordShopTest")

    @sanic_app.get("/")
    def basic(request):
        return response.json({'hello': 'worldd'})

    return sanic_app

def test_basic_test_client(app):
    request, response = app.test_client.get("/")

    assert request.method.lower() == "get"
    assert response.body == b'{"hello":"worldd"}'
    assert response.status == 200
