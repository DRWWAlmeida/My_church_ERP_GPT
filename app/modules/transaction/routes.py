from flask import Blueprint, jsonify, request

from app.modules.transaction import services


transaction_bp = Blueprint("transaction", __name__)


@transaction_bp.post("/transaction")
def create():
    data = services.create_transaction(request.get_json(silent=True))
    return jsonify(data=data, status="success", message="Lançamento criado!"), 201


@transaction_bp.get("/transaction")
def list_transactions():
    data, pagination = services.get_transactions(request.args)
    return jsonify(data=data, pagination=pagination, status="success", message="Lançamentos consultados com sucesso!")


@transaction_bp.get("/transaction/<int:transaction_id>")
def get(transaction_id):
    return jsonify(data=services.get_transaction(transaction_id), status="success", message="Lançamento consultado com sucesso!")


@transaction_bp.route("/transaction/<int:transaction_id>", methods=["PUT", "PATCH"])
def update(transaction_id):
    data = services.update_transaction(transaction_id, request.get_json(silent=True), partial=request.method == "PATCH")
    return jsonify(data=data, status="success", message="Lançamento atualizado!")


@transaction_bp.delete("/transaction/<int:transaction_id>")
def delete(transaction_id):
    services.delete_transaction(transaction_id)
    return "", 204
