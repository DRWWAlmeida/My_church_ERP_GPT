import pytest
import os
from app import create_app
from app.scripts.schema import create_schema

@pytest.fixture
def client():
    app = create_app()

    test_db_path = "app/db/igreja_erp_test.db"

    if os.path.exists(test_db_path):
        os.remove(test_db_path)

    app.config.update({'TESTING': True, 'DATABASE': test_db_path})

    with app.app_context():
        create_schema()

    with app.test_client() as client:
        yield client

    if os.path.exists(test_db_path):
        os.remove(test_db_path)