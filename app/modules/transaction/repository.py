import logging
import sqlite3
from contextlib import contextmanager

from app.core.database import get_connection
from app.core.errors import IntegrityError, NotFoundError, OperationalError
from app.modules.transaction.schema import FIELDS, validate_payload


logger = logging.getLogger(__name__)
RELATIONS = {
    "tipo_lancamento_id": "tipo_lancamento",
    "categoria_id": "categoria",
    "conta_corrente_id": "conta_corrente",
}
SELECT = """
    SELECT l.*, t.nome AS tipo_nome, c.nome AS categoria_nome,
           a.nome AS conta_nome
    FROM lancamento l
    JOIN tipo_lancamento t ON t.id = l.tipo_lancamento_id
    JOIN categoria c ON c.id = l.categoria_id
    JOIN conta_corrente a ON a.id = l.conta_corrente_id
"""


@contextmanager
def database(write=False):
    connection = None
    try:
        connection = get_connection()
        connection.row_factory = sqlite3.Row
        connection.execute("BEGIN IMMEDIATE" if write else "BEGIN")
        yield connection
        connection.commit()
    except sqlite3.IntegrityError as error:
        raise IntegrityError("Os dados do lançamento violam a integridade do banco.") from error
    except sqlite3.Error as error:
        logger.exception("Falha ao acessar lançamentos")
        raise OperationalError("Falha operacional ao acessar o banco de dados.") from error
    finally:
        if connection is not None:
            if connection.in_transaction:
                connection.rollback()
            connection.close()


def serialize(row):
    return {
        "id": row["id"], "data": row["data"],
        "valor_centavos": row["valor_centavos"], "descricao": row["descricao"],
        "tipo_lancamento": {"id": row["tipo_lancamento_id"], "nome": row["tipo_nome"]},
        "categoria": {"id": row["categoria_id"], "nome": row["categoria_nome"]},
        "conta_corrente": {"id": row["conta_corrente_id"], "nome": row["conta_nome"]},
    }


def find(connection, transaction_id):
    row = connection.execute(SELECT + " WHERE l.id = ?", (transaction_id,)).fetchone()
    if row is None:
        raise NotFoundError("Lançamento não encontrado.")
    return row


def check_relations(connection, payload):
    for field, table in RELATIONS.items():
        if connection.execute(f"SELECT 1 FROM {table} WHERE id = ?", (payload[field],)).fetchone() is None:
            raise IntegrityError(f"O registro informado em '{field}' não existe.", field=field, value=payload[field])


def create(payload):
    with database(write=True) as connection:
        check_relations(connection, payload)
        cursor = connection.execute(
            f"INSERT INTO lancamento ({', '.join(FIELDS)}) VALUES (?, ?, ?, ?, ?, ?)",
            tuple(payload[field] for field in FIELDS),
        )
        return serialize(find(connection, cursor.lastrowid))


def get(transaction_id):
    with database() as connection:
        return serialize(find(connection, transaction_id))


def update(transaction_id, payload):
    with database(write=True) as connection:
        previous = find(connection, transaction_id)
        merged = {field: previous[field] for field in FIELDS}
        merged.update(payload)
        merged = validate_payload(merged)
        check_relations(connection, merged)
        connection.execute(
            f"UPDATE lancamento SET {', '.join(field + ' = ?' for field in FIELDS)} WHERE id = ?",
            (*[merged[field] for field in FIELDS], transaction_id),
        )
        return serialize(find(connection, transaction_id))


def delete(transaction_id):
    with database(write=True) as connection:
        find(connection, transaction_id)
        connection.execute("DELETE FROM lancamento WHERE id = ?", (transaction_id,))


def list_transactions(filters):
    conditions, params = [], []
    for field in RELATIONS:
        if field in filters:
            conditions.append(f"l.{field} = ?")
            params.append(filters[field])
    for field, operator in (("data_inicio", ">="), ("data_fim", "<=")):
        if field in filters:
            conditions.append(f"l.data {operator} ?")
            params.append(filters[field])
    if "descricao" in filters:
        conditions.append("l.descricao LIKE ? ESCAPE '\\'")
        escaped = filters["descricao"].replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        params.append(f"%{escaped}%")
    where = " WHERE " + " AND ".join(conditions) if conditions else ""
    page, size = filters["page"], filters["per_page"]
    with database() as connection:
        total = connection.execute("SELECT COUNT(*) FROM lancamento l" + where, params).fetchone()[0]
        rows = connection.execute(
            SELECT + where + " ORDER BY l.data DESC, l.id DESC LIMIT ? OFFSET ?",
            (*params, size, (page - 1) * size),
        ).fetchall()
        return [serialize(row) for row in rows], {
            "page": page, "per_page": size, "total": total,
            "total_pages": (total + size - 1) // size,
        }
