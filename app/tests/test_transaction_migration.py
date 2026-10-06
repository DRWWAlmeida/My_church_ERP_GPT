import sqlite3

import pytest

from app.scripts import schema


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


def test_migration_rounding_sequence_idempotence_and_foreign_keys(legacy):
    for index, value in enumerate(('0.29', '1.005', '125.90'), 1):
        insert_legacy(legacy, value, index)
    insert_legacy(legacy, '10.00', 50)
    legacy.execute('DELETE FROM lancamento WHERE id = 50')
    legacy.commit()
    schema.create_schema()
    schema.create_schema()
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
    insert_legacy(legacy, amount)
    legacy.execute("INSERT INTO categoria VALUES (2, 'oferta')")
    legacy.commit()
    before = legacy.execute('SELECT * FROM lancamento').fetchall()
    with pytest.raises(ValueError, match='lançamento 1'):
        schema.create_schema()
    assert legacy.execute('SELECT * FROM lancamento').fetchall() == before
    assert legacy.execute('SELECT COUNT(*) FROM categoria').fetchone()[0] == 2
    assert 'valor' in {row[1] for row in legacy.execute('PRAGMA table_info(lancamento)')}
    assert not legacy.execute("SELECT 1 FROM sqlite_master WHERE name = 'lancamento_centavos'").fetchone()


def test_orphan_relation_aborts_migration(legacy):
    legacy.execute('PRAGMA foreign_keys = OFF')
    insert_legacy(legacy, '10.00')
    legacy.execute('UPDATE lancamento SET categoria_id = 999')
    legacy.commit()
    legacy.execute('PRAGMA foreign_keys = ON')
    with pytest.raises(sqlite3.IntegrityError):
        schema.create_schema()
    assert legacy.execute('SELECT valor, categoria_id FROM lancamento').fetchone() == (10, 999)
