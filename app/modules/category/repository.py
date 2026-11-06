import logging
import sqlite3

from app.core.database import get_connection
from app.core.errors import IntegrityError, OperationalError


logger = logging.getLogger(__name__)


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
        logger.warning("Falha de integridade ao criar categoria: %s", e)
        error = str(e)

        if "UNIQUE constraint failed" in error:
            raise IntegrityError(
                message=f"A categoria '{category_name}' já está cadastrada.",
                field="categoria",
                value=category_name,
            ) from e

        if "NOT NULL constraint failed" in error:
            raise IntegrityError(
                message="O nome da categoria não pode ser vazio.",
                field="categoria",
                value=category_name,
            ) from e

        raise IntegrityError(
            message=f"Esta categoria já está cadastrada ou é inválida. Detalhe: {e}",
            field="categoria",
            value=category_name,
        ) from e

    except sqlite3.OperationalError as e:
        if connection:
            connection.rollback()
        logger.exception("Falha operacional ao criar categoria")
        raise OperationalError(
            message="Falha operacional ao acessar o banco de dados."
        ) from e

    except sqlite3.Error as e:
        if connection:
            connection.rollback()
        logger.exception("Falha inesperada ao criar categoria")
        raise OperationalError(message="Erro inesperado no banco de dados.") from e
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return {"id": id_gerado, "nome": category_name}

def get_category_filters(conditions, params):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        sql = '''SELECT id, nome FROM categoria'''

        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        sql += " ORDER BY id"

        cursor.execute(sql, tuple(params))

        return cursor.fetchall()
    except sqlite3.Error as e:
        logger.exception("Falha ao consultar categorias")
        raise OperationalError(
            message="Falha operacional ao acessar o banco de dados."
        ) from e
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
