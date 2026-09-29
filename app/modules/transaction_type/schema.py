from app.core.errors import ValidationError
from app.core.validators import (
    ensure_length,
    ensure_not_blank,
    ensure_not_none,
    ensure_type,
    normalize_string,
)


def validate_create_transaction_type_payload(payload):
    if not isinstance(payload, dict):
        raise ValidationError("O corpo da requisição deve ser um objeto JSON válido.")

    field_name = "tipo_lancamento"
    transaction_type_name = payload.get(field_name)

    ensure_not_none(transaction_type_name, field_name)
    ensure_type(transaction_type_name, str, field_name)

    transaction_type_name = normalize_string(transaction_type_name)

    ensure_not_blank(transaction_type_name, field_name)
    ensure_length(transaction_type_name, field_name, min_length=3, max_length=100)
    return {field_name: transaction_type_name}


def validate_transaction_type_filters(
    transaction_type_id=None,
    transaction_type_name=None,
):
    parsed_id = None
    if transaction_type_id is not None:
        try:
            parsed_id = int(transaction_type_id)
        except (TypeError, ValueError):
            raise ValidationError(
                message="O campo 'id' deve ser um número inteiro positivo.",
                field="id",
                value=transaction_type_id,
            )

        if parsed_id <= 0:
            raise ValidationError(
                message="O campo 'id' deve ser um número inteiro positivo.",
                field="id",
                value=transaction_type_id,
            )

    parsed_name = None
    if transaction_type_name is not None:
        parsed_name = normalize_string(transaction_type_name)
        ensure_not_blank(parsed_name, "nome")
        ensure_length(parsed_name, "nome", max_length=100)

    return {"id": parsed_id, "nome": parsed_name}
