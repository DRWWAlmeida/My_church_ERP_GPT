import logging
import sqlite3

from app.core.database import get_connection
from app.core.errors import IntegrityError, OperationalError


logger = logging.getLogger(__name__)


def create(transaction_type_name):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO tipo_lancamento (nome) VALUES (?)",
            (transaction_type_name,),
        )
        transaction_type_id = cursor.lastrowid
        connection.commit()
    except sqlite3.IntegrityError as error:
        if connection:
            connection.rollback()
        logger.warning("Falha de integridade ao criar tipo de lançamento: %s", error)

        if "UNIQUE constraint failed" in str(error):
            raise IntegrityError(
                message=(
                    f"O tipo de lançamento '{transaction_type_name}' "
                    "já está cadastrado."
                ),
                field="tipo_lancamento",
                value=transaction_type_name,
            ) from error

        raise IntegrityError(
            message="O tipo de lançamento informado é inválido.",
            field="tipo_lancamento",
            value=transaction_type_name,
        ) from error
    except sqlite3.Error as error:
        if connection:
            connection.rollback()
        logger.exception("Falha ao criar tipo de lançamento")
        raise OperationalError(
            message="Falha operacional ao acessar o banco de dados."
        ) from error
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return {"id": transaction_type_id, "nome": transaction_type_name}


def get_with_filters(conditions, params):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        sql = "SELECT id, nome FROM tipo_lancamento"
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        sql += " ORDER BY id"

        cursor.execute(sql, tuple(params))
        return cursor.fetchall()
    except sqlite3.Error as error:
        logger.exception("Falha ao consultar tipos de lançamento")
        raise OperationalError(
            message="Falha operacional ao acessar o banco de dados."
        ) from error
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
