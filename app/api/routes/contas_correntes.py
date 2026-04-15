from flask import Blueprint, jsonify, request
from app.db.connections import get_connection

contas_correntes_bp = Blueprint("contas_correntes", __name__)


@contas_correntes_bp.get("/contas_correntes")
def contas_correntes():
    return jsonify({"Msg": "Pagina deverá mostrar as contas correntes cadastradas"})

@contas_correntes_bp.route("/register_conta_corrente", methods=['POST'])
def register_conta_corrente():
    dados = request.get_json()
    conta_corrente = dados.get('conta_corrente')

    if not isinstance(conta_corrente, str) or not conta_corrente:
        return jsonify({'mensagem': 'O nome da conta é obrigatório e deve ser um texto.'}), 400
    if len(conta_corrente) < 3 or len(conta_corrente) > 100:
        return jsonify({'mensagem': 'O nome deve ter entre 3 e 100 caracteres.'}), 400
    
    sql = 'INSERT INTO conta_corrente (nome) VALUES (?)'
    try:
        conta_corrente.strip()
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (conta_corrente,))
        connection.commit()
        return jsonify({'mensagem': 'conta_corrente criada', 'seu_dado': dados}), 201
    except Exception as e:
        connection.rollback()
        return jsonify({'ERRO': e})
    finally:
        connection.close()