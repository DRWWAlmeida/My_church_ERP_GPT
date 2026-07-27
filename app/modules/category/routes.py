from flask import Blueprint, jsonify, request
from app.modules.category.services import create_category, get_all_category


category_bp = Blueprint('category', __name__)


@category_bp.route('/category', methods=['GET'])
def category_get():
    response = get_all_category()
    return jsonify({
        "data": response,
        "status": "success",
        "message": "Todas as categorias cadastradas!"
    }), 201

@category_bp.route('/category', methods=['POST'])
def category_bp_post():
    payload = request.get_json()
    response = create_category(payload)
    return jsonify({
        "data": response,
        "status": "success",
        "message": "Categoria criada!"
    }), 201
    

