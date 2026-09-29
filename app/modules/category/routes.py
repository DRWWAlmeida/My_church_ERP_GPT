from flask import Blueprint, jsonify, request

from app.modules.category.schema import validate_category_filters
from app.modules.category.services import create_category, get_category


category_bp = Blueprint('category', __name__)


@category_bp.route('/category', methods=['GET'])
def category_get():
    filters = validate_category_filters(
        category_id=request.args.get('id'),
        category_name=request.args.get('nome'),
    )

    response = get_category(filters["id"], filters["nome"])
    return jsonify({
        "data": response,
        "status": "success",
        "message": "Categorias consultadas com sucesso!"
    }), 200


@category_bp.route('/category', methods=['POST'])
def category_bp_post():
    payload = request.get_json(silent=True)
    response = create_category(payload)
    return jsonify({
        "data": response,
        "status": "success",
        "message": "Categoria criada!"
    }), 201

