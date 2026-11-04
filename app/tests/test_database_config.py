import runpy
import sqlite3
from pathlib import Path
from unittest.mock import Mock

import pytest
from flask import Flask, current_app

from app import create_app
import app.config as config
from app.core import database
from app.scripts import schema


@pytest.fixture(autouse=True)
def protect_local_database(monkeypatch):
    original_connect = sqlite3.connect
    local_database = (config.BASE_DIR / 'db' / 'igreja_erp.db').resolve()

    def guarded_connect(target, *args, **kwargs):
        if isinstance(target, (str, Path)) and Path(target).resolve() == local_database:
            raise AssertionError('Tests must not access the local database')
        return original_connect(target, *args, **kwargs)

    monkeypatch.setattr(sqlite3, 'connect', guarded_connect)


@pytest.mark.parametrize('use_environment', [False, True])
def test_environment_and_factory_without_database_access(monkeypatch, tmp_path, use_environment):
    monkeypatch.delenv('DATABASE_PATH', raising=False)
    if use_environment:
        monkeypatch.setenv('DATABASE_PATH', str(tmp_path / 'environment.db'))
    settings = runpy.run_path(config.__file__)
    expected = str(tmp_path / 'environment.db') if use_environment else str(config.BASE_DIR / 'db' / 'igreja_erp.db')
    assert settings['DB_PATH'] == expected
    monkeypatch.setattr(config, 'DB_PATH', settings['DB_PATH'])
    connect = Mock(side_effect=AssertionError('factory must not connect'))
    monkeypatch.setattr(database.sqlite3, 'connect', connect)
    app = create_app()
    assert app.config['DB_PATH'] == expected
    assert 'DATABASE' not in app.config
    connect.assert_not_called()


@pytest.mark.parametrize('explicit_override', [False, True])
def test_schema_and_api_use_same_target(monkeypatch, tmp_path, explicit_override):
    selected, sentinel = tmp_path / 'selected.db', tmp_path / 'sentinel.db'
    sentinel.write_bytes(b'synthetic-sentinel')
    monkeypatch.setattr(config, 'DB_PATH', sentinel)
    app = create_app()
    app.config.update(TESTING=True, DB_PATH=sentinel if explicit_override else selected)
    if explicit_override:
        app.config['DATABASE'] = selected
    with app.app_context():
        schema.create_schema()
    with app.test_client() as client:
        assert client.post('/category', json={'categoria': 'Oferta'}).status_code == 201
        assert client.get('/category').json['data'] == [{'id': 1, 'nome': 'Oferta'}]
    assert sentinel.read_bytes() == b'synthetic-sentinel'
    with sqlite3.connect(selected) as connection:
        assert connection.execute('SELECT nome FROM categoria').fetchall() == [('Oferta',)]


def test_without_context_reads_current_module_configuration(monkeypatch, tmp_path):
    target = tmp_path / 'outside.db'
    monkeypatch.setattr(config, 'DB_PATH', target)
    connection = database.get_connection()
    try:
        assert connection.execute('PRAGMA foreign_keys').fetchone()[0] == 1
        assert connection.execute('PRAGMA database_list').fetchone()[2] == str(target)
    finally:
        connection.close()


def test_app_contexts_keep_databases_separate(tmp_path):
    apps = [create_app(), create_app()]
    for index, app in enumerate(apps):
        app.config.update(TESTING=True, DATABASE=tmp_path / f'app-{index}.db')
        with app.app_context():
            schema.create_schema()
        with app.test_client() as client:
            assert client.post('/category', json={'categoria': f'Conta {index}'}).status_code == 201
    for index in (1, 0, 1):
        with apps[index].test_client() as client:
            assert client.get('/category').json['data'] == [{'id': 1, 'nome': f'Conta {index}'}]


@pytest.mark.parametrize('key', ['DATABASE', 'DB_PATH'])
@pytest.mark.parametrize('value', [None, '', '  ', 123, False, []])
def test_invalid_explicit_target_never_connects(monkeypatch, key, value):
    app = create_app()
    app.config[key] = value
    connect = Mock()
    monkeypatch.setattr(database.sqlite3, 'connect', connect)
    with app.app_context(), pytest.raises(ValueError, match='banco'):
        database.get_connection()
    connect.assert_not_called()


def test_import_entrypoint_has_no_database_or_server_side_effects(monkeypatch):
    prepare, connect, serve = Mock(), Mock(), Mock()
    monkeypatch.setattr(schema, 'create_schema', prepare)
    monkeypatch.setattr(database.sqlite3, 'connect', connect)
    monkeypatch.setattr(Flask, 'run', serve)
    module = runpy.run_module('app.run', run_name='test_import')
    assert isinstance(module['app'], Flask)
    prepare.assert_not_called()
    connect.assert_not_called()
    serve.assert_not_called()


def test_main_prepares_context_before_serving(monkeypatch, tmp_path):
    monkeypatch.setattr(config, 'DB_PATH', tmp_path / 'default.db')
    module = runpy.run_module('app.run', run_name='test_main')
    app = module['app']
    app.config.update(DATABASE=tmp_path / 'selected.db', DEBUG=False, TESTING=True)
    events = []
    prepare = schema.create_schema

    def observed_prepare():
        assert current_app._get_current_object() is app
        events.append('schema')
        prepare()

    def serve(**kwargs):
        assert events == ['schema']
        assert kwargs == {'debug': False}
        with app.test_client() as client:
            assert client.post('/category', json={'categoria': 'Oferta'}).status_code == 201
        events.append('serve')

    monkeypatch.setitem(module['main'].__globals__, 'create_schema', observed_prepare)
    monkeypatch.setattr(app, 'run', serve)
    module['main']()
    assert events == ['schema', 'serve']
    assert not (tmp_path / 'default.db').exists()


def test_schema_failure_prevents_server(monkeypatch):
    module = runpy.run_module('app.run', run_name='test_failure')
    fail = Mock(side_effect=RuntimeError('synthetic-schema-failure'))
    serve = Mock()
    monkeypatch.setitem(module['main'].__globals__, 'create_schema', fail)
    monkeypatch.setattr(module['app'], 'run', serve)
    with pytest.raises(RuntimeError, match='synthetic-schema-failure'):
        module['main']()
    serve.assert_not_called()


def test_missing_parent_prevents_server_without_fallback(monkeypatch, tmp_path):
    fallback = tmp_path / 'fallback.db'
    monkeypatch.setattr(config, 'DB_PATH', fallback)
    module = runpy.run_module('app.run', run_name='test_missing_parent')
    module['app'].config['DATABASE'] = tmp_path / 'missing' / 'target.db'
    serve = Mock()
    monkeypatch.setattr(module['app'], 'run', serve)
    with pytest.raises(sqlite3.OperationalError):
        module['main']()
    serve.assert_not_called()
    assert not fallback.exists()
    assert not (tmp_path / 'missing').exists()
