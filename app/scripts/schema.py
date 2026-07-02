from app.core.database import get_connection

def create_schema():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conta_corrente(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                nome VARCHAR(100) NOT NULL)
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tipo_lancamento(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(100) NOT NULL)
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categoria(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(100) NOT NULL)
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
        connection.commit()
    finally:
        connection.close()

