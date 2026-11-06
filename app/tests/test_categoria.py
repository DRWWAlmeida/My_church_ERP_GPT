import pytest


@pytest.fixture
def created_categories(client):
    names = ["Tecnologia", "Luz", "Uso e Consumo"]
    for name in names:
        response = client.post("/category", json={"categoria": name})
        assert response.status_code == 201
    return names


@pytest.mark.parametrize("category", ["Tecnologia", "Luz", "Uso e Consumo"])
def test_success_create_category(client, category):
    response = client.post("/category", json={"categoria": category})
    payload = response.get_json()

    assert response.status_code == 201
    assert payload == {
        "data": {"id": 1, "nome": category},
        "message": "Categoria criada!",
        "status": "success",
    }


def test_missing_category_field(client):
    response = client.post("/category", json={"category": ""})
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["status"] == "error"
    assert payload["message"] == "O campo 'categoria' é obrigatório."


@pytest.mark.parametrize("body", [None, [], "categoria"])
def test_rejects_body_that_is_not_json_object(client, body):
    if body is None:
        response = client.post("/category", data="invalid", content_type="application/json")
    else:
        response = client.post("/category", json=body)

    payload = response.get_json()
    assert response.status_code == 400
    assert payload["message"] == "O corpo da requisição deve ser um objeto JSON válido."


@pytest.mark.parametrize("characters_quantity", [1, 2])
def test_rejects_short_category(client, characters_quantity):
    short_category = "a" * characters_quantity
    response = client.post("/category", json={"categoria": short_category})
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["message"] == "O campo 'categoria' deve ter no mínimo 3 caracteres."
    assert payload["data"]["categoria"] == short_category


@pytest.mark.parametrize("characters_quantity", [101, 120, 150, 200, 300])
def test_rejects_long_category(client, characters_quantity):
    response = client.post(
        "/category", json={"categoria": "a" * characters_quantity}
    )

    assert response.status_code == 400
    assert response.get_json()["status"] == "error"


def test_rejects_non_string_category(client):
    response = client.post("/category", json={"categoria": 1})

    assert response.status_code == 400
    assert response.get_json()["status"] == "error"


def test_rejects_duplicate_category_ignoring_case(client):
    first_response = client.post("/category", json={"categoria": "Oferta"})
    duplicate_response = client.post("/category", json={"categoria": "oferta"})
    payload = duplicate_response.get_json()

    assert first_response.status_code == 201
    assert duplicate_response.status_code == 400
    assert payload["message"] == "A categoria 'oferta' já está cadastrada."


def test_get_all_categories(client, created_categories):
    response = client.get("/category")
    payload = response.get_json()

    assert response.status_code == 200
    assert [category["nome"] for category in payload["data"]] == created_categories


def test_get_category_by_id(client, created_categories):
    response = client.get("/category?id=2")

    assert response.status_code == 200
    assert response.get_json()["data"] == [{"id": 2, "nome": "Luz"}]


def test_get_category_by_partial_name(client, created_categories):
    response = client.get("/category?nome=uso")

    assert response.status_code == 200
    assert response.get_json()["data"] == [{"id": 3, "nome": "Uso e Consumo"}]


def test_get_category_combines_filters(client, created_categories):
    response = client.get("/category?id=1&nome=tec")

    assert response.status_code == 200
    assert response.get_json()["data"] == [{"id": 1, "nome": "Tecnologia"}]


def test_get_category_returns_empty_list(client):
    response = client.get("/category?nome=inexistente")

    assert response.status_code == 200
    assert response.get_json()["data"] == []


@pytest.mark.parametrize("category_id", ["abc", "0", "-1", "1.5"])
def test_rejects_invalid_category_id(client, category_id):
    response = client.get(f"/category?id={category_id}")
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["status"] == "error"
    assert payload["data"]["id"] == category_id


def test_rejects_blank_name_filter(client):
    response = client.get("/category?nome=%20%20")

    assert response.status_code == 400
    assert response.get_json()["message"] == "O campo 'nome' não pode ser vazio."
