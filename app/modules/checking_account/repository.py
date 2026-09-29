import logging
import sqlite3

from app.core.database import get_connection
from app.core.errors import IntegrityError, OperationalError


logger = logging.getLogger(__name__)


def create(account_name):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO conta_corrente (nome) VALUES (?)",
            (account_name,),
        )
        account_id = cursor.lastrowid
        connection.commit()
    except sqlite3.IntegrityError as error:
        if connection:
            connection.rollback()
        logger.warning("Falha de integridade ao criar conta corrente: %s", error)

        if "UNIQUE constraint failed" in str(error):
            raise IntegrityError(
                message=f"A conta corrente '{account_name}' já está cadastrada.",
                field="conta_corrente",
                value=account_name,
            ) from error

        raise IntegrityError(
            message="A conta corrente informada é inválida.",
            field="conta_corrente",
            value=account_name,
        ) from error
    except sqlite3.Error as error:
        if connection:
            connection.rollback()
        logger.exception("Falha ao criar conta corrente")
        raise OperationalError(
            message="Falha operacional ao acessar o banco de dados."
        ) from error
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return {"id": account_id, "nome": account_name}


def get_with_filters(conditions, params):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        sql = "SELECT id, nome FROM conta_corrente"
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        sql += " ORDER BY id"

        cursor.execute(sql, tuple(params))
        return cursor.fetchall()
    except sqlite3.Error as error:
        logger.exception("Falha ao consultar contas correntes")
        raise OperationalError(
            message="Falha operacional ao acessar o banco de dados."
        ) from error
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
