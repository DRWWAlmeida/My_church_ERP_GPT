"""Atomic upgrade from SQLite decimal affinity to integer cents."""
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


def migrate_transaction_values(connection):
    columns = {row[1] for row in connection.execute("PRAGMA table_info(lancamento)")}
    if "valor_centavos" not in columns:
        # Validate every legacy amount before changing the table.
        converted = []
        for row in connection.execute(
            "SELECT id, tipo_lancamento_id, data, valor, descricao, categoria_id, conta_corrente_id FROM lancamento"
        ):
            try:
                amount = Decimal(str(row[3]))
                if not amount.is_finite() or amount <= 0:
                    raise ValueError("Valor não positivo ou não finito")
                cents = int((amount * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
                if not 1 <= cents <= 9223372036854775807:
                    raise ValueError("Valor fora do intervalo suportado")
            except (InvalidOperation, ValueError, OverflowError) as error:
                raise ValueError(f"Migração interrompida: valor inválido no lançamento {row[0]}.") from error
            converted.append((*row[:3], cents, *row[4:]))

        sequence = connection.execute(
            "SELECT seq FROM sqlite_sequence WHERE name = 'lancamento'"
        ).fetchone()
        connection.execute("""
            CREATE TABLE lancamento_centavos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_lancamento_id INTEGER NOT NULL REFERENCES tipo_lancamento(id),
                data DATE NOT NULL,
                valor_centavos INTEGER NOT NULL
                    CHECK(typeof(valor_centavos) = 'integer' AND valor_centavos > 0),
                descricao TEXT NOT NULL,
                categoria_id INTEGER NOT NULL REFERENCES categoria(id),
                conta_corrente_id INTEGER NOT NULL REFERENCES conta_corrente(id)
            )
        """)
        connection.executemany(
            "INSERT INTO lancamento_centavos VALUES (?, ?, ?, ?, ?, ?, ?)", converted
        )
        connection.execute("DROP TABLE lancamento")
        connection.execute("ALTER TABLE lancamento_centavos RENAME TO lancamento")
        if sequence:
            connection.execute("DELETE FROM sqlite_sequence WHERE name = 'lancamento'")
            connection.execute("INSERT INTO sqlite_sequence(name, seq) VALUES ('lancamento', ?)", sequence)

    for column in ("data", "tipo_lancamento_id", "categoria_id", "conta_corrente_id"):
        connection.execute(f"CREATE INDEX IF NOT EXISTS ix_lancamento_{column} ON lancamento({column})")
