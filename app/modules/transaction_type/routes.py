from flask import Blueprint, jsonify, request

from app.modules.transaction_type.schema import validate_transaction_type_filters
from app.modules.transaction_type.services import (
    create_transaction_type,
    get_transaction_types,
)


transaction_type_bp = Blueprint("transaction_type", __name__)


@transaction_type_bp.route("/transaction-type", methods=["GET"])
def transaction_type_get():
    filters = validate_transaction_type_filters(
        transaction_type_id=request.args.get("id"),
        transaction_type_name=request.args.get("nome"),
    )

    response = get_transaction_types(filters["id"], filters["nome"])
    return jsonify({
        "data": response,
        "status": "success",
        "message": "Tipos de lançamento consultados com sucesso!",
    }), 200


@transaction_type_bp.route("/transaction-type", methods=["POST"])
def transaction_type_post():
    payload = request.get_json(silent=True)
    response = create_transaction_type(payload)
    return jsonify({
        "data": response,
        "status": "success",
        "message": "Tipo de lançamento criado!",
    }), 201
