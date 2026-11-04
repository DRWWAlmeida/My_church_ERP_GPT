"""Shared HTTP guarantees for the three financial registries."""
import sqlite3

import pytest

from app.core.database import get_connection
from app.modules.category import repository as categories
from app.modules.checking_account import repository as accounts
from app.modules.transaction_type import repository as types


@pytest.fixture(params=[
    ("/category", "categoria", "categoria", categories),
    ("/checking-account", "conta_corrente", "conta_corrente", accounts),
    ("/transaction-type", "tipo_lancamento", "tipo_lancamento", types),
], ids=["category", "checking-account", "transaction-type"])
def registry(request):
    return request.param


@pytest.mark.parametrize("length", [3, 100])
def test_trimmed_name_boundaries_round_trip(client, registry, length):
    url, field, _, _ = registry
    name = "A" * length
    created = client.post(url, json={field: f"  {name}  "})
    assert created.status_code == 201
    body = created.get_json()
    assert body["status"] == "success"
    assert isinstance(body["message"], str) and body["message"]
    assert body["data"]["nome"] == name
    record_id = body["data"]["id"]
    assert isinstance(record_id, int) and record_id > 0

    found = client.get(url, query_string={"id": record_id, "nome": "aaa"})
    assert found.status_code == 200
    assert found.get_json()["status"] == "success"
    assert found.get_json()["data"] == [body["data"]]
    empty = client.get(url, query_string={"id": record_id, "nome": "missing"})
    assert empty.status_code == 200
    assert empty.get_json()["data"] == []


def test_rejections_preserve_existing_records(client, registry):
    url, field, _, _ = registry
    created = client.post(url, json={field: "Oferta"})
    assert created.status_code == 201
    original = created.get_json()["data"]
    invalid_bodies = [[], {}, {field: None}, {field: 123}, {field: "  "},
                      {field: "ab"}, {field: "a" * 101}, {field: "oferta"}]
    for payload in invalid_bodies:
        response = client.post(url, json=payload)
        assert response.status_code == 400
        assert response.get_json()["status"] == "error"
        assert response.get_json()["message"]
        assert client.get(url).get_json()["data"] == [original]


@pytest.mark.parametrize("method", ["get", "post"])
@pytest.mark.parametrize("error_type", [sqlite3.OperationalError, sqlite3.DatabaseError])
def test_database_failures_are_generic_json(client, registry, monkeypatch, method, error_type):
    url, field, _, repository = registry

    def fail():
        raise error_type("synthetic-private-path SELECT internal_table")

    monkeypatch.setattr(repository, "get_connection", fail)
    response = getattr(client, method)(url, json={field: "Oferta"})
    assert response.status_code == 500
    body = response.get_json()
    assert body["status"] == "error"
    assert isinstance(body["message"], str) and body["message"]
    assert "synthetic-private-path" not in response.get_data(as_text=True)
    assert "SELECT internal_table" not in response.get_data(as_text=True)


def test_integrity_failure_hides_database_detail_and_does_not_write(client, registry):
    url, field, table, _ = registry
    # Only the isolated fixture database is modified. The table is from this test's allowlist.
    with client.application.app_context():
        connection = get_connection()
        try:
            connection.execute(f"""
                CREATE TRIGGER reject_synthetic_insert BEFORE INSERT ON {table}
                BEGIN
                    SELECT RAISE(ABORT, 'synthetic-private-constraint');
                END
            """)
            connection.commit()
        finally:
            connection.close()

    response = client.post(url, json={field: "Oferta"})
    assert response.status_code == 400
    body = response.get_json()
    assert body["status"] == "error"
    assert body["message"]
    assert body["data"] == {field: "Oferta"}
    assert "synthetic-private-constraint" not in response.get_data(as_text=True)
    assert client.get(url).get_json()["data"] == []
