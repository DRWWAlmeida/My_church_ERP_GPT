from app.core.errors import ValidationError
from app.core.validators import (
    ensure_length,
    ensure_not_blank,
    ensure_not_none,
    ensure_type,
    normalize_string,
)


def validate_create_checking_account_payload(payload):
    if not isinstance(payload, dict):
        raise ValidationError("O corpo da requisição deve ser um objeto JSON válido.")

    field_name = "conta_corrente"
    account_name = payload.get(field_name)

    ensure_not_none(account_name, field_name)
    ensure_type(account_name, str, field_name)

    account_name = normalize_string(account_name)

    ensure_not_blank(account_name, field_name)
    ensure_length(account_name, field_name, min_length=3, max_length=100)
    return {field_name: account_name}


def validate_checking_account_filters(account_id=None, account_name=None):
    parsed_id = None
    if account_id is not None:
        try:
            parsed_id = int(account_id)
        except (TypeError, ValueError):
            raise ValidationError(
                message="O campo 'id' deve ser um número inteiro positivo.",
                field="id",
                value=account_id,
            )

        if parsed_id <= 0:
            raise ValidationError(
                message="O campo 'id' deve ser um número inteiro positivo.",
                field="id",
                value=account_id,
            )

    parsed_name = None
    if account_name is not None:
        parsed_name = normalize_string(account_name)
        ensure_not_blank(parsed_name, "nome")
        ensure_length(parsed_name, "nome", max_length=100)

    return {"id": parsed_id, "nome": parsed_name}
