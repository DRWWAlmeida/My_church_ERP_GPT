import pytest


@pytest.fixture
def created_transaction_types(client):
    names = ["Entrada", "Saída", "Transferência"]
    for name in names:
        response = client.post(
            "/transaction-type",
            json={"tipo_lancamento": name},
        )
        assert response.status_code == 201
    return names


def test_create_transaction_type(client):
    response = client.post(
        "/transaction-type",
        json={"tipo_lancamento": "  Entrada  "},
    )

    assert response.status_code == 201
    assert response.get_json() == {
        "data": {"id": 1, "nome": "Entrada"},
        "message": "Tipo de lançamento criado!",
        "status": "success",
    }


@pytest.mark.parametrize("body", [None, [], "tipo"])
def test_rejects_body_that_is_not_json_object(client, body):
    if body is None:
        response = client.post(
            "/transaction-type",
            data="invalid",
            content_type="application/json",
        )
    else:
        response = client.post("/transaction-type", json=body)

    assert response.status_code == 400
    assert response.get_json()["message"] == (
        "O corpo da requisição deve ser um objeto JSON válido."
    )


@pytest.mark.parametrize(
    ("payload", "expected_message"),
    [
        ({}, "O campo 'tipo_lancamento' é obrigatório."),
        (
            {"tipo_lancamento": 1},
            "O campo 'tipo_lancamento' deve ser do tipo str.",
        ),
        (
            {"tipo_lancamento": "  "},
            "O campo 'tipo_lancamento' não pode ser vazio.",
        ),
        (
            {"tipo_lancamento": "ab"},
            "O campo 'tipo_lancamento' deve ter no mínimo 3 caracteres.",
        ),
        (
            {"tipo_lancamento": "a" * 101},
            "O campo 'tipo_lancamento' deve ter no máximo 100 caracteres.",
        ),
    ],
)
def test_rejects_invalid_transaction_type(client, payload, expected_message):
    response = client.post("/transaction-type", json=payload)

    assert response.status_code == 400
    assert response.get_json()["message"] == expected_message


def test_rejects_duplicate_transaction_type_ignoring_case(client):
    first_response = client.post(
        "/transaction-type",
        json={"tipo_lancamento": "Entrada"},
    )
    duplicate_response = client.post(
        "/transaction-type",
        json={"tipo_lancamento": "entrada"},
    )

    assert first_response.status_code == 201
    assert duplicate_response.status_code == 400
    assert duplicate_response.get_json()["message"] == (
        "O tipo de lançamento 'entrada' já está cadastrado."
    )


def test_get_all_transaction_types(client, created_transaction_types):
    response = client.get("/transaction-type")

    assert response.status_code == 200
    assert [item["nome"] for item in response.get_json()["data"]] == (
        created_transaction_types
    )


def test_get_transaction_type_by_id(client, created_transaction_types):
    response = client.get("/transaction-type?id=2")

    assert response.status_code == 200
    assert response.get_json()["data"] == [{"id": 2, "nome": "Saída"}]


def test_get_transaction_type_by_partial_name(client, created_transaction_types):
    response = client.get("/transaction-type?nome=trans")

    assert response.status_code == 200
    assert response.get_json()["data"] == [{"id": 3, "nome": "Transferência"}]


def test_get_transaction_type_combines_filters(client, created_transaction_types):
    response = client.get("/transaction-type?id=1&nome=entrada")

    assert response.status_code == 200
    assert response.get_json()["data"] == [{"id": 1, "nome": "Entrada"}]


def test_get_transaction_type_returns_empty_list(client):
    response = client.get("/transaction-type?nome=inexistente")

    assert response.status_code == 200
    assert response.get_json()["data"] == []


@pytest.mark.parametrize("transaction_type_id", ["abc", "0", "-1", "1.5"])
def test_rejects_invalid_transaction_type_id(client, transaction_type_id):
    response = client.get(f"/transaction-type?id={transaction_type_id}")

    assert response.status_code == 400
    assert response.get_json()["data"]["id"] == transaction_type_id


def test_rejects_blank_transaction_type_name_filter(client):
    response = client.get("/transaction-type?nome=%20%20")

    assert response.status_code == 400
    assert response.get_json()["message"] == "O campo 'nome' não pode ser vazio."
