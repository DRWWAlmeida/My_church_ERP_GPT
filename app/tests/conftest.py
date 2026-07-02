import pytest
from app import create_app
from app.scripts.schema import create_schema

@pytest.fixture
def client():
    app = create_app()
    create_schema()

    app.config.update({'TESTING': True})

    with app.test_client() as client:
        yield client