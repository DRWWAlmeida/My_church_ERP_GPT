import re
from datetime import date

from app.core.errors import ValidationError


MAX_INTEGER = 9223372036854775807
RELATIONS = ("tipo_lancamento_id", "categoria_id", "conta_corrente_id")
FIELDS = (*RELATIONS, "data", "valor_centavos", "descricao")


def invalid(field, value, message):
    raise ValidationError(message, field=field, value=value)


def positive_integer(value, field, maximum=MAX_INTEGER):
    if type(value) is not int or not 1 <= value <= maximum:
        invalid(field, value, f"O campo '{field}' deve ser um inteiro entre 1 e {maximum}.")
    return value


def iso_date(value, field):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
        invalid(field, value, f"O campo '{field}' deve usar o formato YYYY-MM-DD.")
    try:
        date.fromisoformat(value)
    except ValueError:
        invalid(field, value, f"O campo '{field}' deve conter uma data válida.")
    return value


def validate_payload(payload, partial=False):
    if not isinstance(payload, dict):
        raise ValidationError("O corpo da requisição deve ser um objeto JSON válido.")
    if not payload:
        raise ValidationError("Informe os campos do lançamento.")
    unknown = set(payload) - set(FIELDS)
    if unknown:
        raise ValidationError(f"Campos desconhecidos: {', '.join(sorted(unknown))}.")
    if not partial:
        for field in FIELDS:
            if field not in payload:
                invalid(field, None, f"O campo '{field}' é obrigatório.")
    result = {}
    for field, value in payload.items():
        if field in RELATIONS or field == "valor_centavos":
            result[field] = positive_integer(value, field)
        elif field == "data":
            result[field] = iso_date(value, field)
        else:
            if not isinstance(value, str) or not 3 <= len(value.strip()) <= 255:
                invalid(field, value, "A descrição deve conter entre 3 e 255 caracteres.")
            result[field] = value.strip()
    return result


def validate_query(args):
    allowed = {*RELATIONS, "data_inicio", "data_fim", "descricao", "page", "per_page"}
    if set(args) - allowed:
        raise ValidationError("Parâmetro de consulta desconhecido.")
    result = {"page": 1, "per_page": 20}
    for field in args:
        if len(args.getlist(field)) != 1:
            raise ValidationError(f"O parâmetro '{field}' não pode ser repetido.")
        value = args[field]
        if field in RELATIONS or field in ("page", "per_page"):
            if not re.fullmatch(r"[0-9]{1,19}", value):
                invalid(field, value, f"O parâmetro '{field}' deve ser um inteiro positivo.")
            result[field] = positive_integer(int(value), field, 100 if field == "per_page" else MAX_INTEGER)
        elif field in ("data_inicio", "data_fim"):
            result[field] = iso_date(value, field)
        else:
            if not value.strip() or len(value.strip()) > 255:
                invalid(field, value, "Informe uma descrição de até 255 caracteres.")
            result[field] = value.strip()
    if result.get("data_inicio", "0000") > result.get("data_fim", "9999"):
        raise ValidationError("A data inicial não pode ser posterior à data final.")
    if (result["page"] - 1) * result["per_page"] > MAX_INTEGER:
        raise ValidationError("Página fora do limite permitido.")
    return result
