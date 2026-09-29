from app.modules.checking_account.repository import create, get_with_filters
from app.modules.checking_account.schema import validate_create_checking_account_payload


def create_checking_account(payload):
    validated_data = validate_create_checking_account_payload(payload)
    return create(validated_data["conta_corrente"])


def get_checking_accounts(account_id, account_name):
    conditions = []
    params = []

    if account_id is not None:
        conditions.append("id = ?")
        params.append(account_id)

    if account_name is not None:
        conditions.append("nome LIKE ?")
        params.append(f"%{account_name}%")

    return [dict(account) for account in get_with_filters(conditions, params)]
