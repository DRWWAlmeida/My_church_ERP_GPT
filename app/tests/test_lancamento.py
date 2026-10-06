import sqlite3

import pytest

from app.modules.transaction import repository


@pytest.fixture
def payload(client):
    for url, field, name in (
        ("category", "categoria", "Oferta"),
        ("checking-account", "conta_corrente", "Caixa"),
        ("transaction-type", "tipo_lancamento", "Entrada"),
    ):
        assert client.post('/' + url, json={field: name}).status_code == 201
    return dict(tipo_lancamento_id=1, categoria_id=1, conta_corrente_id=1,
                data="2026-10-06", valor_centavos=12590, descricao="Oferta semanal")


def test_full_lifecycle(client, payload):
    created = client.post('/transaction', json={**payload, "descricao": "  Oferta semanal  "})
    assert created.status_code == 201
    data = created.json['data']
    assert data == {
        "id": 1, "data": "2026-10-06", "valor_centavos": 12590,
        "descricao": "Oferta semanal",
        "tipo_lancamento": {"id": 1, "nome": "Entrada"},
        "categoria": {"id": 1, "nome": "Oferta"},
        "conta_corrente": {"id": 1, "nome": "Caixa"},
    }
    assert client.get('/transaction/1').json['data'] == data
    put = client.put('/transaction/1', json={**payload, "valor_centavos": 1})
    assert put.status_code == 200
    assert put.json['data']['valor_centavos'] == 1
    patch = client.patch('/transaction/1', json={"descricao": "Alterada"})
    assert patch.status_code == 200
    assert patch.json['data']['descricao'] == "Alterada"
    assert patch.json['data']['valor_centavos'] == 1
    deleted = client.delete('/transaction/1')
    assert deleted.status_code == 204 and deleted.data == b''
    assert client.get('/transaction/1').status_code == 404
    assert client.delete('/transaction/1').status_code == 404


@pytest.mark.parametrize('field,value', [
    ('valor_centavos', v) for v in (0, -1, 1.5, True, '100', None, 2**63)
] + [
    ('data', v) for v in ('2026-02-30', '06/10/2026', '20261006', None)
] + [
    ('descricao', v) for v in ('  ', 'ab', 'x' * 256, 123, None)
] + [
    (field, v) for field in repository.RELATIONS for v in (True, 0, -1, 1.5, '1', None, 2**63)
])
def test_invalid_fields(client, payload, field, value):
    response = client.post('/transaction', json={**payload, field: value})
    assert response.status_code == 400
    assert response.json['status'] == 'error'
    assert client.get('/transaction').json['pagination']['total'] == 0


@pytest.mark.parametrize('body', ['null', '[]', 'true', '123', '"texto"', '{', '{}'])
def test_invalid_body(client, body):
    assert client.post('/transaction', data=body, content_type='application/json').status_code == 400


@pytest.mark.parametrize('field', repository.FIELDS)
def test_required_fields(client, payload, field):
    payload.pop(field)
    assert client.post('/transaction', json=payload).status_code == 400


@pytest.mark.parametrize('field', repository.RELATIONS)
def test_invalid_relation_does_not_write(client, payload, field):
    assert client.post('/transaction', json={**payload, field: 999}).status_code == 400
    client.post('/transaction', json=payload)
    response = client.patch('/transaction/1', json={field: 999, 'descricao': 'Alterada'})
    assert response.status_code == 400
    assert response.json['data'][field] == 999
    assert client.get('/transaction/1').json['data']['descricao'] == payload['descricao']


def test_update_contract(client, payload):
    client.post('/transaction', json=payload)
    assert client.put('/transaction/1', json={'descricao': 'Alterada'}).status_code == 400
    assert client.patch('/transaction/1', json={}).status_code == 400
    assert client.patch('/transaction/1', json={'id': 2}).status_code == 400
    assert client.put('/transaction/999', json=payload).status_code == 404
    assert client.patch('/transaction/999', json={'descricao': 'Alterada'}).status_code == 404


def test_future_date_and_changed_relations(client, payload):
    client.post('/transaction-type', json={'tipo_lancamento': 'Saída'})
    client.post('/category', json={'categoria': 'Despesas'})
    client.post('/checking-account', json={'conta_corrente': 'Banco'})
    client.post('/transaction', json=payload)
    response = client.patch('/transaction/1', json={
        'data': '2099-12-31', 'tipo_lancamento_id': 2,
        'categoria_id': 2, 'conta_corrente_id': 2,
    })
    assert response.status_code == 200
    assert response.json['data']['tipo_lancamento']['nome'] == 'Saída'
    assert response.json['data']['categoria']['nome'] == 'Despesas'
    assert response.json['data']['conta_corrente']['nome'] == 'Banco'
    assert response.json['data']['valor_centavos'] > 0


def test_filters_pagination_and_order(client, payload):
    for day in ('2026-10-05', '2026-10-06', '2026-10-06'):
        assert client.post('/transaction', json={**payload, 'data': day}).status_code == 201
    page = client.get('/transaction?per_page=2').json
    assert [r['id'] for r in page['data']] == [3, 2]
    assert page['pagination'] == dict(page=1, per_page=2, total=3, total_pages=2)
    assert [r['id'] for r in client.get('/transaction?page=2&per_page=2').json['data']] == [1]
    assert client.get('/transaction?page=3&per_page=2').json['data'] == []
    query = '/transaction?data_inicio=2026-10-06&data_fim=2026-10-06&tipo_lancamento_id=1&categoria_id=1&conta_corrente_id=1&descricao=semanal'
    assert client.get(query).json['pagination']['total'] == 2
    for field in repository.RELATIONS:
        assert client.get('/transaction?' + field + '=999').json['data'] == []
    assert client.get('/transaction?descricao=%25').json['data'] == []
    assert client.get("/transaction?descricao=' OR 1=1 --").json['data'] == []


@pytest.mark.parametrize('query', [
    'page=0', 'page=abc', 'per_page=101', 'page=9223372036854775807',
    'categoria_id=0', 'tipo_lancamento_id=abc', 'conta_corrente_id=-1',
    'data_inicio=2026-02-30', 'data_inicio=2026-10-07&data_fim=2026-10-06',
    'descricao=', 'descricao=' + 'x'*256, 'unknown=1', 'page=1&page=2',
])
def test_invalid_query(client, query):
    assert client.get('/transaction?' + query).status_code == 400


@pytest.mark.parametrize('method,url', [('get', '/transaction'), ('post', '/transaction'), ('patch', '/transaction/1'), ('delete', '/transaction/1')])
def test_database_failure_json(client, payload, monkeypatch, method, url):
    def fail():
        raise sqlite3.OperationalError('private database path')
    monkeypatch.setattr(repository, 'get_connection', fail)
    response = getattr(client, method)(url, json=payload)
    assert response.status_code == 500
    assert response.json['status'] == 'error'
    assert 'private' not in response.get_data(as_text=True)
