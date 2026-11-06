from app.modules.transaction_type.repository import create, get_with_filters
from app.modules.transaction_type.schema import validate_create_transaction_type_payload


def create_transaction_type(payload):
    validated_data = validate_create_transaction_type_payload(payload)
    return create(validated_data["tipo_lancamento"])


def get_transaction_types(transaction_type_id, transaction_type_name):
    conditions = []
    params = []

    if transaction_type_id is not None:
        conditions.append("id = ?")
        params.append(transaction_type_id)

    if transaction_type_name is not None:
        conditions.append("nome LIKE ?")
        params.append(f"%{transaction_type_name}%")

    return [
        dict(transaction_type)
        for transaction_type in get_with_filters(conditions, params)
    ]
