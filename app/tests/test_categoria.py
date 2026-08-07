from app.modules.category.services import create_category
from app.core.errors import ValidationError
import pytest

@pytest.fixture
def create_category(client):
    response = client.post('/category', json={'categoria': 'Tecnologia'})

@pytest.mark.parametrize('category', [('Tecnologia'), ('Luz'), ("Uso e Consumo"), ])
def test_success_create_category(client, category):
    response = client.post('/category', json={'categoria': category})
    payload = response.get_json()

    assert response.status_code == 201
    assert payload['status'] == 'success'

def test_category_field_empty(client):
    empty_category_field = ""
    response = client.post('/category', json={'category': empty_category_field})
    payload = response.get_json()

    assert response.status_code == 400
    assert payload['status'] == 'error'
    assert payload['message'] == "O campo 'categoria' é obrigatório."

@pytest.mark.parametrize("caracters_quantity", [(1), (2)])
def test_fail_create_category(client, caracters_quantity):
    short_category = 'a'*caracters_quantity
    response = client.post('/category', json={'categoria': short_category})
    payload = response.get_json()

    assert response.status_code == 400
    assert payload['status'] == 'error'
    assert payload['message'] == "O campo 'categoria' deve ter no mínimo 3 caracteres."
    assert payload["data"]['categoria'] == short_category

@pytest.mark.parametrize('caracters_quantity', [(101), (120), (150), (200), (300)])
def test_fail_create_long_category(client, caracters_quantity):
    long_category = 'a'*caracters_quantity
    response = client.post('/category', json={'categoria': long_category})
    payload = response.get_json()

    assert response.status_code == 400
    assert payload['status'] == 'error'

def test_fail_create_category_int(client):
    response = client.post('/category', json={'categoria': 1})
    payload = response.get_json()

    assert response.status_code == 400
    assert payload['status'] == 'error'

def test_get_all_category(client, create_category):
    create_category
    print(create_category)
    response = client.get('/category')
    payload = response.get_json()

    assert response.status_code == 201
    assert payload['status'] == 'success'



