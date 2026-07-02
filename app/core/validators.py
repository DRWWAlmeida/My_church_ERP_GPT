from app.core.errors import ValidationError

def ensure_not_none(value, field_name):
    if value is None:
        raise ValidationError(
            message=f"O campo '{field_name}' é obrigatório.",
            field=field_name,
            value=value,
        )
    return value

def ensure_type(value, expected_type, field_name):
    if not isinstance(value, expected_type):
        raise ValidationError(
            message=f"O campo '{field_name}' deve ser do tipo {expected_type.__name__}.",
            field=field_name,
            value=value,
        )
    return value

def normalize_string(value):
    return value.strip()

def ensure_not_blank(value, field_name):
    if value == "":
        raise ValidationError(
            message=f"O campo '{field_name}' não pode ser vazio.",
            field=field_name,
            value=value,
        )
    return value

def ensure_length(value, field_name, min_length=None, max_length=None):
    size = len(value)

    if min_length is not None and size < min_length:
        raise ValidationError(
            message=f"O campo '{field_name}' deve ter no mínimo {min_length} caracteres.",
            field=field_name,
            value=value,
        )

    if max_length is not None and size > max_length:
        raise ValidationError(
            message=f"O campo '{field_name}' deve ter no máximo {max_length} caracteres.",
            field=field_name,
            value=value,
        )

    return value


