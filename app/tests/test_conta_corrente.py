import pytest


@pytest.fixture
def created_accounts(client):
    names = ["Banco Principal", "Caixa", "Conta Digital"]
    for name in names:
        response = client.post(
            "/checking-account",
            json={"conta_corrente": name},
        )
        assert response.status_code == 201
    return names


def test_create_checking_account(client):
    response = client.post(
        "/checking-account",
        json={"conta_corrente": "  Banco Principal  "},
    )

    assert response.status_code == 201
    assert response.get_json() == {
        "data": {"id": 1, "nome": "Banco Principal"},
        "message": "Conta corrente criada!",
        "status": "success",
    }


@pytest.mark.parametrize("body", [None, [], "conta"])
def test_rejects_body_that_is_not_json_object(client, body):
    if body is None:
        response = client.post(
            "/checking-account",
            data="invalid",
            content_type="application/json",
        )
    else:
        response = client.post("/checking-account", json=body)

    assert response.status_code == 400
    assert response.get_json()["message"] == (
        "O corpo da requisição deve ser um objeto JSON válido."
    )


@pytest.mark.parametrize(
    ("payload", "expected_message"),
    [
        ({}, "O campo 'conta_corrente' é obrigatório."),
        ({"conta_corrente": 1}, "O campo 'conta_corrente' deve ser do tipo str."),
        ({"conta_corrente": "  "}, "O campo 'conta_corrente' não pode ser vazio."),
        (
            {"conta_corrente": "ab"},
            "O campo 'conta_corrente' deve ter no mínimo 3 caracteres.",
        ),
        (
            {"conta_corrente": "a" * 101},
            "O campo 'conta_corrente' deve ter no máximo 100 caracteres.",
        ),
    ],
)
def test_rejects_invalid_checking_account(client, payload, expected_message):
    response = client.post("/checking-account", json=payload)

    assert response.status_code == 400
    assert response.get_json()["message"] == expected_message


def test_rejects_duplicate_checking_account_ignoring_case(client):
    first_response = client.post(
        "/checking-account",
        json={"conta_corrente": "Banco Principal"},
    )
    duplicate_response = client.post(
        "/checking-account",
        json={"conta_corrente": "banco principal"},
    )

    assert first_response.status_code == 201
    assert duplicate_response.status_code == 400
    assert duplicate_response.get_json()["message"] == (
        "A conta corrente 'banco principal' já está cadastrada."
    )


def test_get_all_checking_accounts(client, created_accounts):
    response = client.get("/checking-account")

    assert response.status_code == 200
    assert [account["nome"] for account in response.get_json()["data"]] == (
        created_accounts
    )


def test_get_checking_account_by_id(client, created_accounts):
    response = client.get("/checking-account?id=2")

    assert response.status_code == 200
    assert response.get_json()["data"] == [{"id": 2, "nome": "Caixa"}]


def test_get_checking_account_by_partial_name(client, created_accounts):
    response = client.get("/checking-account?nome=digital")

    assert response.status_code == 200
    assert response.get_json()["data"] == [{"id": 3, "nome": "Conta Digital"}]


def test_get_checking_account_combines_filters(client, created_accounts):
    response = client.get("/checking-account?id=1&nome=principal")

    assert response.status_code == 200
    assert response.get_json()["data"] == [{"id": 1, "nome": "Banco Principal"}]


def test_get_checking_account_returns_empty_list(client):
    response = client.get("/checking-account?nome=inexistente")

    assert response.status_code == 200
    assert response.get_json()["data"] == []


@pytest.mark.parametrize("account_id", ["abc", "0", "-1", "1.5"])
def test_rejects_invalid_checking_account_id(client, account_id):
    response = client.get(f"/checking-account?id={account_id}")

    assert response.status_code == 400
    assert response.get_json()["data"]["id"] == account_id


def test_rejects_blank_checking_account_name_filter(client):
    response = client.get("/checking-account?nome=%20%20")

    assert response.status_code == 400
    assert response.get_json()["message"] == "O campo 'nome' não pode ser vazio."
