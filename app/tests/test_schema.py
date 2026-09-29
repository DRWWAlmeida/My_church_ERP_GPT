import sqlite3
from uuid import uuid4

from app import create_app
from app.scripts.schema import create_schema


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
