import pytest
from uuid import uuid4

from app import create_app
from app.scripts.schema import create_schema


@pytest.fixture
def client():
    app = create_app()
    test_db_path = app.config["BASE_DIR"] / "db" / f"test_{uuid4().hex}.db"

    app.config.update({"TESTING": True, "DATABASE": str(test_db_path)})

    with app.app_context():
        create_schema()

    try:
        with app.test_client() as client:
            yield client
    finally:
        test_db_path.unlink(missing_ok=True)
