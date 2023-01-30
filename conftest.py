import pytest
from api import create_app

@pytest.fixture
def app():
    app = create_app()
    yield app

@pytest.fixture
def client(app):
    with app.app_context():
        yield app.test_client()
