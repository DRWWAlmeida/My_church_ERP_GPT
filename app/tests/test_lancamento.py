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
    ('data', v) for v in ('2026-02-30', '2025-02-29', '06/10/2026', '20261006', None)
] + [
    ('descricao', v) for v in ('  ', 'ab', 'x' * 256, 123, None)
] + [
    (field, v) for field in repository.RELATIONS for v in (True, 0, -1, 1.5, '1', None, 2**63)
])
def test_invalid_fields(client, payload, field, value):
    created = client.post('/transaction', json=payload)
    assert created.status_code == 201
    original = created.json['data']
    response = client.post('/transaction', json={**payload, field: value})
    assert response.status_code == 400
    assert response.json['status'] == 'error'
    listing = client.get('/transaction').json
    assert listing['pagination']['total'] == 1
    assert listing['data'] == [original]


@pytest.mark.parametrize('body', ['null', '[]', 'true', '123', '"texto"', '{', '{}'])
def test_invalid_body(client, body):
    response = client.post('/transaction', data=body, content_type='application/json')
    assert response.status_code == 400
    assert response.json['status'] == 'error'
    assert client.get('/transaction').json['pagination']['total'] == 0


@pytest.mark.parametrize('field', repository.FIELDS)
def test_required_fields(client, payload, field):
    payload.pop(field)
    response = client.post('/transaction', json=payload)
    assert response.status_code == 400
    assert response.json['status'] == 'error'
    assert client.get('/transaction').json['pagination']['total'] == 0


@pytest.mark.parametrize('field', repository.RELATIONS)
def test_invalid_relation_does_not_write(client, payload, field):
    assert client.post('/transaction', json={**payload, field: 999}).status_code == 400
    assert client.get('/transaction').json['pagination']['total'] == 0
    client.post('/transaction', json=payload)
    response = client.patch('/transaction/1', json={field: 999, 'descricao': 'Alterada'})
    assert response.status_code == 400
    assert response.json['data'][field] == 999
    assert client.get('/transaction/1').json['data']['descricao'] == payload['descricao']


@pytest.mark.parametrize('amount,description_length,day', [
    (1, 3, '2024-02-29'),
    (12590, 255, '2099-12-31'),
    (9223372036854775807, 3, '2026-10-06'),
])
def test_create_boundaries_round_trip(client, payload, amount, description_length, day):
    description = 'x' * description_length
    response = client.post('/transaction', json={
        **payload, 'valor_centavos': amount, 'data': day,
        'descricao': f'  {description}  ',
    })
    assert response.status_code == 201
    assert response.json['status'] == 'success'
    assert response.json['message']
    created = response.json['data']
    assert created['valor_centavos'] == amount
    assert type(created['valor_centavos']) is int
    assert created['descricao'] == description
    assert created['data'] == day
    read = client.get(f"/transaction/{created['id']}")
    assert read.status_code == 200
    assert read.json['data'] == created


def test_create_outgoing_keeps_positive_amount_and_one_record(client, payload):
    transaction_type = client.post('/transaction-type', json={'tipo_lancamento': 'Saída'})
    assert transaction_type.status_code == 201
    response = client.post('/transaction', json={
        **payload, 'tipo_lancamento_id': transaction_type.json['data']['id'],
    })
    assert response.status_code == 201
    created = response.json['data']
    assert created['tipo_lancamento'] == transaction_type.json['data']
    assert created['valor_centavos'] == payload['valor_centavos']
    assert client.get('/transaction').json['data'] == [created]
    assert client.get('/checking-account').json['data'] == [{'id': 1, 'nome': 'Caixa'}]


def test_create_unknown_field_preserves_existing_record(client, payload):
    created = client.post('/transaction', json=payload)
    assert created.status_code == 201
    response = client.post('/transaction', json={**payload, 'unknown': 'value'})
    assert response.status_code == 400
    assert response.json['status'] == 'error'
    listing = client.get('/transaction').json
    assert listing['pagination']['total'] == 1
    assert listing['data'] == [created.json['data']]


def test_update_contract(client, payload):
    created = client.post('/transaction', json=payload)
    assert created.status_code == 201
    original = created.json['data']
    assert client.put('/transaction/1', json={'descricao': 'Alterada'}).status_code == 400
    assert client.patch('/transaction/1', json={}).status_code == 400
    assert client.patch('/transaction/1', json={'id': 2}).status_code == 400
    assert client.put('/transaction/999', json=payload).status_code == 404
    assert client.patch('/transaction/999', json={'descricao': 'Alterada'}).status_code == 404
    assert client.get('/transaction').json['data'] == [original]


def test_put_replaces_all_fields_and_patch_preserves_omitted_fields(client, payload):
    created = client.post('/transaction', json=payload)
    assert created.status_code == 201
    replacement = dict(payload, data='2099-12-31', valor_centavos=1, descricao='Nova oferta')
    relations = {}
    for url, field, relation in [
        ('transaction-type', 'tipo_lancamento', 'tipo_lancamento'),
        ('category', 'categoria', 'categoria'),
        ('checking-account', 'conta_corrente', 'conta_corrente'),
    ]:
        response = client.post('/' + url, json={field: 'Alternativa'})
        assert response.status_code == 201
        relations[relation] = response.json['data']
        replacement[relation + '_id'] = response.json['data']['id']
    url = f"/transaction/{created.json['data']['id']}"
    response = client.put(url, json=replacement)
    expected = dict(id=created.json['data']['id'], data='2099-12-31',
                    valor_centavos=1, descricao='Nova oferta', **relations)
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['data'] == expected
    assert client.get(url).json['data'] == expected
    patched = client.patch(url, json={'descricao': '  Ajustada  '})
    expected['descricao'] = 'Ajustada'
    assert patched.status_code == 200
    assert patched.json['data'] == expected
    assert client.get(url).json['data'] == expected


def test_delete_preserves_other_transactions_and_relations(client, payload):
    first = client.post('/transaction', json=payload)
    second = client.post('/transaction', json={**payload, 'descricao': 'Outro registro'})
    assert first.status_code == second.status_code == 201
    url = f"/transaction/{first.json['data']['id']}"
    response = client.delete(url)
    assert response.status_code == 204 and response.data == b''
    for response in (client.get(url), client.delete(url)):
        assert response.status_code == 404
        assert response.json['status'] == 'error'
    listing = client.get('/transaction').json
    assert listing['data'] == [second.json['data']]
    assert listing['pagination']['total'] == 1
    for endpoint in ('category', 'checking-account', 'transaction-type'):
        assert len(client.get('/' + endpoint).json['data']) == 1


@pytest.mark.parametrize('method', ['post', 'put', 'patch', 'delete'])
@pytest.mark.parametrize('error_type,status', [
    (sqlite3.OperationalError, 500), (sqlite3.IntegrityError, 400),
])
def test_write_is_rolled_back_when_commit_fails(client, payload, monkeypatch, method, error_type, status):
    created = client.post('/transaction', json=payload)
    assert created.status_code == 201
    original = created.json['data']
    db_path = client.application.config['DATABASE']
    pending_rows = []

    class FailingCommitConnection(sqlite3.Connection):
        def commit(self):
            # Real SQL has already modified this transaction, before commit is rejected.
            assert self.in_transaction
            assert self.total_changes > 0
            pending_rows.extend(tuple(row) for row in self.execute(
                'SELECT id, descricao FROM lancamento ORDER BY id'
            ))
            raise error_type('synthetic-private-commit-detail')

    def failing_connection():
        connection = sqlite3.connect(db_path, factory=FailingCommitConnection)
        connection.execute('PRAGMA foreign_keys = ON')
        return connection

    url = '/transaction' if method == 'post' else f"/transaction/{original['id']}"
    with monkeypatch.context() as scoped:
        scoped.setattr(repository, 'get_connection', failing_connection)
        response = getattr(client, method)(url, json={**payload, 'descricao': 'Tentativa'})
    assert response.status_code == status
    assert response.json['status'] == 'error'
    assert 'synthetic-private-commit-detail' not in response.get_data(as_text=True)
    expected_pending = {
        'post': [(original['id'], payload['descricao']), (original['id'] + 1, 'Tentativa')],
        'put': [(original['id'], 'Tentativa')],
        'patch': [(original['id'], 'Tentativa')],
        'delete': [],
    }
    assert pending_rows == expected_pending[method]
    # A fresh connection through the API must see only the committed original.
    listing = client.get('/transaction').json
    assert listing['data'] == [original]
    assert listing['pagination']['total'] == 1
    # A subsequent write also proves that no connection retained a write lock.
    retry = client.patch(f"/transaction/{original['id']}", json={'descricao': 'Recuperada'})
    assert retry.status_code == 200
    assert client.get(f"/transaction/{original['id']}").json['data']['descricao'] == 'Recuperada'


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
    response = client.get('/transaction?' + query)
    assert response.status_code == 400
    assert response.json['status'] == 'error'


def test_individual_missing_transaction_returns_json(client):
    response = client.get('/transaction/9223372036854775807')
    assert response.status_code == 404
    assert response.json['status'] == 'error'
    assert response.json['message']


def test_combined_filters_exclude_each_nonmatching_record(client, payload):
    for url, field in [('transaction-type', 'tipo_lancamento'),
                       ('category', 'categoria'), ('checking-account', 'conta_corrente')]:
        assert client.post('/' + url, json={field: 'Alternativa'}).status_code == 201
    expected = []
    for day in ('2026-10-05', '2026-10-07'):
        response = client.post('/transaction', json={**payload, 'data': day})
        assert response.status_code == 201
        expected.insert(0, response.json['data'])
    # Each distractor differs in exactly one filter, exposing an omitted condition.
    for change in [
        {'tipo_lancamento_id': 2}, {'categoria_id': 2}, {'conta_corrente_id': 2},
        {'data': '2026-10-04'}, {'data': '2026-10-08'}, {'descricao': 'Outra oferta'},
    ]:
        assert client.post('/transaction', json={**payload, **change}).status_code == 201
    response = client.get('/transaction', query_string={
        'tipo_lancamento_id': 1, 'categoria_id': 1, 'conta_corrente_id': 1,
        'data_inicio': '2026-10-05', 'data_fim': '2026-10-07', 'descricao': 'semanal',
        'per_page': 1,
    })
    assert response.status_code == 200
    assert response.json['data'] == expected[:1]
    assert response.json['pagination'] == dict(page=1, per_page=1, total=2, total_pages=2)


@pytest.mark.parametrize('literal,lookalike', [('%', 'percentual'), ('_', 'X'), ('\\', '/')])
def test_description_search_matches_literal_characters(client, payload, literal, lookalike):
    matching = client.post('/transaction', json={**payload, 'descricao': f'Oferta {literal} mensal'})
    assert matching.status_code == 201
    assert client.post('/transaction', json={**payload, 'descricao': f'Oferta {lookalike} mensal'}).status_code == 201
    response = client.get('/transaction', query_string={'descricao': literal})
    assert response.status_code == 200
    assert response.json['data'] == [matching.json['data']]
    assert response.json['pagination']['total'] == 1


def test_default_pagination_and_maximum_page_size(client, payload):
    ids = []
    for _ in range(21):
        created = client.post('/transaction', json=payload)
        assert created.status_code == 201
        ids.insert(0, created.json['data']['id'])
    first = client.get('/transaction')
    assert first.status_code == 200
    assert [row['id'] for row in first.json['data']] == ids[:20]
    assert first.json['pagination'] == dict(page=1, per_page=20, total=21, total_pages=2)
    last = client.get('/transaction?page=2')
    assert last.status_code == 200
    assert [row['id'] for row in last.json['data']] == ids[20:]
    assert last.json['pagination'] == dict(page=2, per_page=20, total=21, total_pages=2)
    beyond = client.get('/transaction?page=3')
    assert beyond.status_code == 200
    assert beyond.json['data'] == []
    assert beyond.json['pagination'] == dict(page=3, per_page=20, total=21, total_pages=2)
    maximum = client.get('/transaction?per_page=100')
    assert maximum.status_code == 200
    assert [row['id'] for row in maximum.json['data']] == ids
    assert maximum.json['pagination'] == dict(page=1, per_page=100, total=21, total_pages=1)


def test_empty_collection_and_largest_supported_offset(client):
    empty = client.get('/transaction')
    assert empty.status_code == 200
    assert empty.json['data'] == []
    assert empty.json['pagination'] == dict(page=1, per_page=20, total=0, total_pages=0)
    # With size 2, this page reaches the largest representable even offset.
    response = client.get('/transaction?page=4611686018427387904&per_page=2')
    assert response.status_code == 200
    assert response.json['data'] == []
    assert response.json['pagination'] == dict(page=4611686018427387904, per_page=2, total=0, total_pages=0)
    overflow = client.get('/transaction?page=4611686018427387905&per_page=2')
    assert overflow.status_code == 400
    assert overflow.json['status'] == 'error'


@pytest.mark.parametrize('field,value', [
    ('tipo_lancamento_id', '1'), ('categoria_id', '1'), ('conta_corrente_id', '1'),
    ('data_inicio', '2026-10-06'), ('data_fim', '2026-10-06'),
    ('descricao', 'Oferta'), ('per_page', '20'),
])
def test_repeated_filters_are_rejected(client, field, value):
    response = client.get('/transaction', query_string=[(field, value), (field, value)])
    assert response.status_code == 400
    assert response.json['status'] == 'error'


@pytest.mark.parametrize('method,url', [('get', '/transaction'), ('post', '/transaction'), ('patch', '/transaction/1'), ('delete', '/transaction/1')])
def test_database_failure_json(client, payload, monkeypatch, method, url):
    def fail():
        raise sqlite3.OperationalError('private database path')
    monkeypatch.setattr(repository, 'get_connection', fail)
    response = getattr(client, method)(url, json=payload)
    assert response.status_code == 500
    assert response.json['status'] == 'error'
    assert 'private' not in response.get_data(as_text=True)
