from flask import jsonify, request, Blueprint
from app.db.connections import get_connection

tipo_lancamentos_bp = Blueprint("tipo_lancamento", __name__)

@tipo_lancamentos_bp.get("/tipo_lancamentos")
def tipo_lancamentos():
    return jsonify({'Pagina': 'GET.tipo_lancamentos'})

@tipo_lancamentos_bp.route("/register_tipo_lancamento", methods=['POST'])
def register_tipo_lancamento():
    dados = request.get_json()
    tipo_lancamento = dados.get('tipo_lancamento')

    if not isinstance(tipo_lancamento, str) or not tipo_lancamento:
        return jsonify({'mensagem': 'O nome do tipo de lançamento é obrigatório e deve ser um texto.'}), 400
    if len(tipo_lancamento) < 5 or len(tipo_lancamento) > 100:
        return jsonify({'mensagem': 'O nome do tipo de lançamento deve ser maior que 5 e menor que 100.'}), 400
    
    sql = 'INSERT INTO tipo_lancamento (nome) VALUES (?)'
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (tipo_lancamento,))
        connection.commit()
        return jsonify({'Mensagem': "Tipo de lançamento salvo com sucesso!", 'tipo_lancamento': tipo_lancamento}), 201
    except Exception as e:
        return jsonify({'ERRO': e})
    finally:
        connection.close()
