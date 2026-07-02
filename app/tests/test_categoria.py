
def test_criar_categoria_com_sucesso(client):
    response = client.post('/category', json={'categoria': 'Tecnologia'})

    assert response.status_code == 201
    assert response.get_json()['status'] == 'success'

def test_falha_criar_categoria_curta(client):
    categoria_curta = 'a'*2
    response = client.post('/category', json={'categoria': categoria_curta})

    assert response.status_code == 400
    assert response.get_json()['status'] == 'error'

def test_falha_criar_categoria_longa(client):
    categoria_curta = 'a'*101
    response = client.post('/category', json={'categoria': categoria_curta})

    assert response.status_code == 400
    assert response.get_json()['status'] == 'error'

def test_falha_criar_categoria_tipo_dado_int(client):
    response = client.post('/category', json={'categoria': 1})

    assert response.status_code == 400
    assert response.get_json()['status'] == 'error'


