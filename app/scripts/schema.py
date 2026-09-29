from app.core.database import get_connection

def create_schema():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conta_corrente(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                nome VARCHAR(100) NOT NULL COLLATE NOCASE UNIQUE)
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tipo_lancamento(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(100) NOT NULL)
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categoria(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(100) NOT NULL COLLATE NOCASE UNIQUE)
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lancamento(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                tipo_lancamento_id INTEGER NOT NULL,
                data DATE NOT NULL,
                valor DECIMAL(10,2) NOT NULL,
                descricao TEXT NOT NULL,
                categoria_id INTEGER NOT NULL,
                conta_corrente_id INTEGER NOT NULL,
                FOREIGN KEY (tipo_lancamento_id) REFERENCES tipo_lancamento(id),
                FOREIGN KEY (categoria_id) REFERENCES categoria(id),
                FOREIGN KEY (conta_corrente_id) REFERENCES conta_corrente(id)
                )
        ''')

        # Preserve the oldest category and repoint existing transactions before
        # enabling uniqueness on databases created by older versions.
        cursor.execute('''
            UPDATE lancamento
            SET categoria_id = (
                SELECT MIN(canonical.id)
                FROM categoria AS canonical
                JOIN categoria AS current
                    ON canonical.nome = current.nome COLLATE NOCASE
                WHERE current.id = lancamento.categoria_id
            )
            WHERE EXISTS (
                SELECT 1 FROM categoria
                WHERE id = lancamento.categoria_id
            )
        ''')
        cursor.execute('''
            DELETE FROM categoria
            WHERE id NOT IN (
                SELECT MIN(id)
                FROM categoria
                GROUP BY nome COLLATE NOCASE
            )
        ''')
        cursor.execute('''
            CREATE UNIQUE INDEX IF NOT EXISTS uq_categoria_nome
            ON categoria(nome COLLATE NOCASE)
        ''')

        # Apply the same migration strategy to legacy checking accounts.
        cursor.execute('''
            UPDATE lancamento
            SET conta_corrente_id = (
                SELECT MIN(canonical.id)
                FROM conta_corrente AS canonical
                JOIN conta_corrente AS current
                    ON canonical.nome = current.nome COLLATE NOCASE
                WHERE current.id = lancamento.conta_corrente_id
            )
            WHERE EXISTS (
                SELECT 1 FROM conta_corrente
                WHERE id = lancamento.conta_corrente_id
            )
        ''')
        cursor.execute('''
            DELETE FROM conta_corrente
            WHERE id NOT IN (
                SELECT MIN(id)
                FROM conta_corrente
                GROUP BY nome COLLATE NOCASE
            )
        ''')
        cursor.execute('''
            CREATE UNIQUE INDEX IF NOT EXISTS uq_conta_corrente_nome
            ON conta_corrente(nome COLLATE NOCASE)
        ''')
        connection.commit()
    finally:
        connection.close()

