from flask import jsonify, request, Blueprint

home_bp = Blueprint('home', __name__)

@home_bp.get("/")
def home():
    return jsonify({"Mensagem": "Hello World"})