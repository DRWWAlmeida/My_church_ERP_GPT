from flask import Blueprint, jsonify, request
from app.db.connections import get_connection

categorias_bp = Blueprint("categorias", __name__)

@categorias_bp.get('/categorias')
def categorias():
    return jsonify({"Msg": "Pagina deverá mostrar as categorias cadastradas"})

@categorias_bp.route("/register_categoria", methods=['POST'])
def register_categoria():
    dados = request.get_json()
    categoria = dados.get('categoria')

    if not isinstance(categoria, str) or not categoria:
        return jsonify({'mensagem': 'O nome da categoria é obrigatório e deve ser um texto.'}), 400
    if len(categoria) < 3 or len(categoria) > 100:
        return jsonify({'mensagem': 'O nome deve ter entre 3 e 100 caracteres.'}), 400
    
    sql = 'INSERT INTO categoria (nome) VALUES (?)'
    try:
        categoria.strip()
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (categoria,))
        connection.commit()
        return jsonify({'mensagem': 'categoria criada', 'seu_dado': dados}), 201
    except Exception as e:
        connection.rollback()
        return jsonify({'ERRO': e})
    finally:
        connection.close()