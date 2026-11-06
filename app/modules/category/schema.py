from app.core.validators import (
    ensure_length,
    ensure_not_blank,
    ensure_not_none,
    ensure_type,
    normalize_string,
)
from app.core.errors import ValidationError


def validate_create_category_payload(payload):
    if not isinstance(payload, dict):
        raise ValidationError("O corpo da requisição deve ser um objeto JSON válido.")
    field_name = 'categoria'
    category_name = payload.get(field_name)

    ensure_not_none(category_name, field_name)
    ensure_type(category_name, str, field_name)

    category_name = normalize_string(category_name)

    ensure_not_blank(category_name, field_name)
    ensure_length(category_name, field_name, min_length=3, max_length=100)
    return {field_name: category_name}


def validate_category_filters(category_id=None, category_name=None):
    parsed_id = None
    if category_id is not None:
        try:
            parsed_id = int(category_id)
        except (TypeError, ValueError):
            raise ValidationError(
                message="O campo 'id' deve ser um número inteiro positivo.",
                field="id",
                value=category_id,
            )

        if parsed_id <= 0:
            raise ValidationError(
                message="O campo 'id' deve ser um número inteiro positivo.",
                field="id",
                value=category_id,
            )

    parsed_name = None
    if category_name is not None:
        parsed_name = normalize_string(category_name)
        ensure_not_blank(parsed_name, "nome")
        ensure_length(parsed_name, "nome", max_length=100)

    return {"id": parsed_id, "nome": parsed_name}

