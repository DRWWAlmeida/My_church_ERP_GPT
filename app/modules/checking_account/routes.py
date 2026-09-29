from flask import Blueprint, jsonify, request

from app.modules.checking_account.schema import validate_checking_account_filters
from app.modules.checking_account.services import (
    create_checking_account,
    get_checking_accounts,
)


checking_account_bp = Blueprint("checking_account", __name__)


@checking_account_bp.route("/checking-account", methods=["GET"])
def checking_account_get():
    filters = validate_checking_account_filters(
        account_id=request.args.get("id"),
        account_name=request.args.get("nome"),
    )

    response = get_checking_accounts(filters["id"], filters["nome"])
    return jsonify({
        "data": response,
        "status": "success",
        "message": "Contas correntes consultadas com sucesso!",
    }), 200


@checking_account_bp.route("/checking-account", methods=["POST"])
def checking_account_post():
    payload = request.get_json(silent=True)
    response = create_checking_account(payload)
    return jsonify({
        "data": response,
        "status": "success",
        "message": "Conta corrente criada!",
    }), 201
