import sqlite3

import pytest

from app.scripts import schema
from app import create_app
from app.core.database import get_connection


class TestConnection(sqlite3.Connection):
    __test__ = False

    def close(self):
        # Keep the in-memory database alive between create_schema calls.
        pass


@pytest.fixture
def legacy(monkeypatch):
    connection = sqlite3.connect(':memory:', factory=TestConnection)
    connection.executescript('''
        PRAGMA foreign_keys = ON;
        CREATE TABLE categoria(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL);
        CREATE TABLE conta_corrente(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL);
        CREATE TABLE tipo_lancamento(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL);
        INSERT INTO categoria VALUES (1, 'Oferta');
        INSERT INTO conta_corrente VALUES (1, 'Caixa');
        INSERT INTO tipo_lancamento VALUES (1, 'Entrada');
        CREATE TABLE lancamento(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_lancamento_id INTEGER NOT NULL REFERENCES tipo_lancamento(id),
            data DATE NOT NULL, valor DECIMAL(10,2) NOT NULL, descricao TEXT NOT NULL,
            categoria_id INTEGER NOT NULL REFERENCES categoria(id),
            conta_corrente_id INTEGER NOT NULL REFERENCES conta_corrente(id)
        );
    ''')
    monkeypatch.setattr(schema, 'get_connection', lambda: connection)
    yield connection
    sqlite3.Connection.close(connection)


def insert_legacy(connection, amount, row_id=1):
    connection.execute(
        "INSERT INTO lancamento VALUES (?, 1, '2026-10-06', ?, 'Oferta', 1, 1)",
        (row_id, amount),
    )
    connection.commit()


def snapshot(connection):
    """Compare all schema objects, rows and AUTOINCREMENT high-water marks."""
    objects = connection.execute(
        'SELECT type, name, tbl_name, sql FROM sqlite_master ORDER BY type, name'
    ).fetchall()
    rows = {
        name: connection.execute(f'SELECT * FROM "{name}" ORDER BY rowid').fetchall()
        for kind, name, _, _ in objects if kind == 'table'
    }
    return objects, rows


def seed_duplicates(connection):
    for table, name in (
        ('categoria', 'oferta'), ('conta_corrente', 'caixa'),
        ('tipo_lancamento', 'entrada'),
    ):
        connection.execute(f'INSERT INTO {table} VALUES (7, ?)', (name,))
    connection.execute(
        'UPDATE lancamento SET categoria_id = 7, conta_corrente_id = 7, tipo_lancamento_id = 7'
    )
    connection.commit()


def test_migration_rounding_sequence_idempotence_and_foreign_keys(legacy):
    for index, value in enumerate(('0.29', '1.005', '125.90'), 1):
        insert_legacy(legacy, value, index)
    insert_legacy(legacy, '10.00', 50)
    legacy.execute('DELETE FROM lancamento WHERE id = 50')
    legacy.commit()
    seed_duplicates(legacy)
    original = legacy.execute('SELECT id, data, descricao FROM lancamento ORDER BY id').fetchall()
    schema.create_schema()
    migrated = snapshot(legacy)
    schema.create_schema()
    assert snapshot(legacy) == migrated
    assert legacy.execute('SELECT id, data, descricao FROM lancamento ORDER BY id').fetchall() == original
    for table, name in (('categoria', 'Oferta'), ('conta_corrente', 'Caixa'), ('tipo_lancamento', 'Entrada')):
        assert legacy.execute(f'SELECT * FROM {table}').fetchall() == [(1, name)]
    assert legacy.execute('SELECT categoria_id, conta_corrente_id, tipo_lancamento_id FROM lancamento').fetchall() == [(1, 1, 1)] * 3
    assert legacy.execute('SELECT id, valor_centavos FROM lancamento ORDER BY id').fetchall() == [(1, 29), (2, 101), (3, 12590)]
    assert legacy.execute('PRAGMA foreign_key_check').fetchall() == []
    assert len(legacy.execute('PRAGMA foreign_key_list(lancamento)').fetchall()) == 3
    cursor = legacy.execute("INSERT INTO lancamento(tipo_lancamento_id, data, valor_centavos, descricao, categoria_id, conta_corrente_id) VALUES (1, '2026-10-06', 1, 'Nova', 1, 1)")
    assert cursor.lastrowid == 51
    for amount in (0, -1, 1.5):
        with pytest.raises(sqlite3.IntegrityError):
            legacy.execute('UPDATE lancamento SET valor_centavos = ? WHERE id = 1', (amount,))
    with pytest.raises(sqlite3.IntegrityError):
        legacy.execute('UPDATE lancamento SET categoria_id = 999 WHERE id = 1')


@pytest.mark.parametrize('amount', ['invalid', '-1', '0', '0.001', 'Infinity', 'NaN', '1e30'])
def test_invalid_legacy_value_rolls_back_entire_upgrade(legacy, amount):
    insert_legacy(legacy, '1.005')
    insert_legacy(legacy, amount, 2)
    seed_duplicates(legacy)
    before = snapshot(legacy)
    with pytest.raises(ValueError, match='lançamento 2'):
        schema.create_schema()
    assert snapshot(legacy) == before
    assert not legacy.in_transaction


@pytest.mark.parametrize('column', ['categoria_id', 'conta_corrente_id', 'tipo_lancamento_id'])
def test_orphan_relation_aborts_migration(legacy, column):
    legacy.execute('PRAGMA foreign_keys = OFF')
    insert_legacy(legacy, '10.00')
    insert_legacy(legacy, '1.005', 2)
    seed_duplicates(legacy)
    legacy.execute(f'UPDATE lancamento SET {column} = 999 WHERE id = 2')
    legacy.commit()
    legacy.execute('PRAGMA foreign_keys = ON')
    before = snapshot(legacy)
    with pytest.raises(sqlite3.IntegrityError):
        schema.create_schema()
    assert snapshot(legacy) == before
    assert not legacy.in_transaction


def test_restore_synthetic_backup_after_committed_migration(legacy, tmp_path, monkeypatch):
    for row_id, amount in enumerate(('0.29', '1.005', '125.90'), 1):
        insert_legacy(legacy, amount, row_id)
    insert_legacy(legacy, '10', 50)
    legacy.execute('DELETE FROM lancamento WHERE id = 50')
    legacy.commit()
    seed_duplicates(legacy)
    before = snapshot(legacy)
    database_path = tmp_path / 'synthetic.db'
    backup_path = tmp_path / 'before-migration.db'
    with sqlite3.connect(database_path) as destination:
        legacy.backup(destination)
    destination.close()
    with sqlite3.connect(database_path) as source, sqlite3.connect(backup_path) as backup:
        source.backup(backup)
        assert snapshot(backup) == before
    source.close()
    backup.close()

    app = create_app()
    app.config.update(TESTING=True, DATABASE=str(database_path))
    monkeypatch.setattr(schema, 'get_connection', get_connection)
    with app.app_context():
        schema.create_schema()
    # A fresh connection proves that conversion committed to disk.
    with sqlite3.connect(database_path) as migrated:
        assert migrated.execute('SELECT valor_centavos FROM lancamento ORDER BY id').fetchall() == [(29,), (101,), (12590,)]
        assert snapshot(migrated) != before
    migrated.close()

    # All application connections are closed before restoring the saved database.
    with sqlite3.connect(backup_path) as backup, sqlite3.connect(database_path) as restored:
        backup.backup(restored)
    backup.close()
    restored.close()
    with sqlite3.connect(database_path) as restored:
        assert snapshot(restored) == before
        assert restored.execute('PRAGMA integrity_check').fetchall() == [('ok',)]
        assert restored.execute('PRAGMA foreign_key_check').fetchall() == []
        cursor = restored.execute("INSERT INTO lancamento(tipo_lancamento_id, data, valor, descricao, categoria_id, conta_corrente_id) VALUES (7, '2026-10-06', 1, 'Restaurado', 7, 7)")
        assert cursor.lastrowid == 51
        restored.rollback()
    restored.close()
