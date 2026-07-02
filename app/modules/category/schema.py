from app.core.validators import (
    ensure_length,
    ensure_not_blank,
    ensure_not_none,
    ensure_type,
    normalize_string,
)
from app.core.errors import ValidationError


def validate_create_category_payload(payload):
    if payload is None:
        raise ValidationError("O corpo da requisição deve ser um JSON válido.")
    field_name = 'categoria'
    category_name = payload.get(field_name)

    ensure_not_none(category_name, field_name)
    ensure_type(category_name, str, field_name)

    category_name = normalize_string(category_name)

    ensure_not_blank(category_name, field_name)
    ensure_length(category_name, field_name, min_length=3, max_length=100)
    return {field_name: category_name}