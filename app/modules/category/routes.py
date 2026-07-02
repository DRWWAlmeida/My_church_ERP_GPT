from flask import Blueprint, jsonify, request
from app.modules.category.services import create_category


category_bp = Blueprint('category', __name__)


@category_bp.route('/category', methods=['GET'])
def category_get():
    return jsonify({"Hello": "World"}), 200

@category_bp.route('/category', methods=['POST'])
def category_bp_post():
    payload = request.get_json()
    response = create_category(payload)
    return jsonify({
        "data": response,
        "status": "success",
        "message": "Categoria criada!"
    }), 201
    

