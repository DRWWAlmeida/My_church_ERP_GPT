from app.core.database import get_connection
from app.core.errors import  OperationalError, IntegrityError
import sqlite3

def create(category_name):
    connection = None
    cursor = None
    id_gerado = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        sql = '''INSERT INTO categoria (nome) VALUES (?)'''
        cursor.execute(sql, (category_name,))

        id_gerado = cursor.lastrowid
        connection.commit()
    except sqlite3.IntegrityError as e:
            if connection:
                connection.rollback()
            print(f"Erro de integridade no SQLite: {e}")
            error = str(e)
            
            if "UNIQUE constraint failed" in error:
                raise IntegrityError(
                    message=f"A categoria '{category_name}' já está cadastrada.",
                    field="categoria",
                    value=category_name,
                )
            
            elif "NOT NULL constraint failed" in error:
                raise IntegrityError(
                    message="O nome da categoria não pode ser vazio.",
                    field="categoria",
                    value=category_name,
                )
            
            else:
                raise IntegrityError(
                message=f"Esta categoria já está cadastrada ou é inválida. Detalhe: {e}", 
                field="categoria", 
                value=category_name,
                )

    except sqlite3.OperationalError as e:
        if connection:
            connection.rollback()
        print(f"Erro operacional no SQLite: {e}")
        raise OperationalError(message=f"Falha operacional ao acessar o banco de dados.")

    except sqlite3.Error as e:
        if connection:
            connection.rollback()
        print(f"Erro genérico de banco de dados: {e}")
        raise OperationalError(message="Erro inesperado no banco de dados.")
    finally:
        if cursor: 
            cursor.close()
        if connection:
            connection.close()

    return {"id": id_gerado, "nome": category_name}