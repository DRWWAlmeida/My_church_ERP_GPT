import sqlite3
from uuid import uuid4

from app import create_app
from app.scripts.schema import create_schema


def seed_missing_relations(connection):
    # Legacy fixtures must contain real FK targets before table reconstruction.
    for table in ("categoria", "conta_corrente", "tipo_lancamento"):
        exists = connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?", (table,)
        ).fetchone()
        if not exists:
            connection.execute(f"CREATE TABLE {table}(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL)")
            connection.execute(f"INSERT INTO {table}(nome) VALUES ('Teste')")


def test_schema_migrates_duplicate_categories_and_preserves_references():
    app = create_app()
    db_path = app.config["BASE_DIR"] / "db" / f"migration_{uuid4().hex}.db"
    connection = sqlite3.connect(db_path)
    try:
        connection.executescript(
            """
            CREATE TABLE categoria(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(100) NOT NULL
            );
            CREATE TABLE lancamento(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_lancamento_id INTEGER NOT NULL,
                data DATE NOT NULL,
                valor DECIMAL(10,2) NOT NULL,
                descricao TEXT NOT NULL,
                categoria_id INTEGER NOT NULL,
                conta_corrente_id INTEGER NOT NULL
            );
            INSERT INTO categoria(nome) VALUES ('Oferta'), ('oferta');
            INSERT INTO lancamento(
                tipo_lancamento_id, data, valor, descricao,
                categoria_id, conta_corrente_id
            ) VALUES (1, '2026-09-28', 10, 'Teste', 2, 1);
            """
        )
        seed_missing_relations(connection)
        connection.commit()
    finally:
        connection.close()

    app.config.update(TESTING=True, DATABASE=str(db_path))
    try:
        with app.app_context():
            create_schema()

        connection = sqlite3.connect(db_path)
        categories = connection.execute(
            "SELECT id, nome FROM categoria ORDER BY id"
        ).fetchall()
        category_id = connection.execute(
            "SELECT categoria_id FROM lancamento"
        ).fetchone()[0]

        assert categories == [(1, "Oferta")]
        assert category_id == 1
    finally:
        if "connection" in locals():
            connection.close()
        db_path.unlink(missing_ok=True)


def test_schema_migrates_duplicate_accounts_and_preserves_references():
    app = create_app()
    db_path = app.config["BASE_DIR"] / "db" / f"migration_{uuid4().hex}.db"
    connection = sqlite3.connect(db_path)
    try:
        connection.executescript(
            """
            CREATE TABLE conta_corrente(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(100) NOT NULL
            );
            CREATE TABLE lancamento(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_lancamento_id INTEGER NOT NULL,
                data DATE NOT NULL,
                valor DECIMAL(10,2) NOT NULL,
                descricao TEXT NOT NULL,
                categoria_id INTEGER NOT NULL,
                conta_corrente_id INTEGER NOT NULL
            );
            INSERT INTO conta_corrente(nome) VALUES ('Caixa'), ('caixa');
            INSERT INTO lancamento(
                tipo_lancamento_id, data, valor, descricao,
                categoria_id, conta_corrente_id
            ) VALUES (1, '2026-09-28', 10, 'Teste', 1, 2);
            """
        )
        seed_missing_relations(connection)
        connection.commit()
    finally:
        connection.close()

    app.config.update(TESTING=True, DATABASE=str(db_path))
    try:
        with app.app_context():
            create_schema()

        connection = sqlite3.connect(db_path)
        accounts = connection.execute(
            "SELECT id, nome FROM conta_corrente ORDER BY id"
        ).fetchall()
        account_id = connection.execute(
            "SELECT conta_corrente_id FROM lancamento"
        ).fetchone()[0]

        assert accounts == [(1, "Caixa")]
        assert account_id == 1
    finally:
        if "connection" in locals():
            connection.close()
        db_path.unlink(missing_ok=True)


def test_schema_migrates_duplicate_transaction_types_and_preserves_references():
    app = create_app()
    db_path = app.config["BASE_DIR"] / "db" / f"migration_{uuid4().hex}.db"
    connection = sqlite3.connect(db_path)
    try:
        connection.executescript(
            """
            CREATE TABLE tipo_lancamento(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(100) NOT NULL
            );
            CREATE TABLE lancamento(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_lancamento_id INTEGER NOT NULL,
                data DATE NOT NULL,
                valor DECIMAL(10,2) NOT NULL,
                descricao TEXT NOT NULL,
                categoria_id INTEGER NOT NULL,
                conta_corrente_id INTEGER NOT NULL
            );
            INSERT INTO tipo_lancamento(nome) VALUES ('Entrada'), ('entrada');
            INSERT INTO lancamento(
                tipo_lancamento_id, data, valor, descricao,
                categoria_id, conta_corrente_id
            ) VALUES (2, '2026-09-28', 10, 'Teste', 1, 1);
            """
        )
        seed_missing_relations(connection)
        connection.commit()
    finally:
        connection.close()

    app.config.update(TESTING=True, DATABASE=str(db_path))
    try:
        with app.app_context():
            create_schema()

        connection = sqlite3.connect(db_path)
        transaction_types = connection.execute(
            "SELECT id, nome FROM tipo_lancamento ORDER BY id"
        ).fetchall()
        transaction_type_id = connection.execute(
            "SELECT tipo_lancamento_id FROM lancamento"
        ).fetchone()[0]

        assert transaction_types == [(1, "Entrada")]
        assert transaction_type_id == 1
    finally:
        if "connection" in locals():
            connection.close()
        db_path.unlink(missing_ok=True)
