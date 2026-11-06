from app.modules.transaction import repository
from app.modules.transaction.schema import positive_integer, validate_payload, validate_query


def create_transaction(payload):
    return repository.create(validate_payload(payload))


def get_transaction(transaction_id):
    return repository.get(positive_integer(transaction_id, "id"))


def get_transactions(args):
    return repository.list_transactions(validate_query(args))


def update_transaction(transaction_id, payload, partial=False):
    positive_integer(transaction_id, "id")
    return repository.update(transaction_id, validate_payload(payload, partial=partial))


def delete_transaction(transaction_id):
    repository.delete(positive_integer(transaction_id, "id"))
