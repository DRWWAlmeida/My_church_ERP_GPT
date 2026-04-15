from flask import Blueprint, jsonify, request
from app.db.connections import get_connection
from datetime import datetime

lancamentos_bp = Blueprint('lancamento', __name__)

@lancamentos_bp.get("/lancamentos")
def lancamentos():
    return jsonify({"Msg": "Pagina deverá mostrar os lancamentos cadastradas"})

@lancamentos_bp.route("/register_lancamento", methods=["POST"])
def register_lancamentos():
    dados = request.get_json() or {}
    
    # 1. Captura dos dados (certifique-se que o frontend envia IDs numéricos)
    tipo_id = dados.get('tipo_lancamento_id')
    data_str = dados.get('data_lancamento')
    valor = dados.get('valor_lancamento')
    descricao = dados.get('descricao_lancamento')
    cat_id = dados.get('categoria_id')
    conta_id = dados.get('conta_corrente_id')

    # 2. Validações de Formato
    # Validar Data
    try:
        datetime.strptime(data_str, '%Y-%m-%d')
    except (ValueError, TypeError):
        return jsonify({'mensagem': 'Data inválida. Use o formato YYYY-MM-DD.'}), 400

    # Validar Valor Numérico
    try:
        valor_float = float(valor)
        if valor_float <= 0:
            return jsonify({'mensagem': 'O valor deve ser maior que zero.'}), 400
    except (ValueError, TypeError):
        return jsonify({'mensagem': 'O valor deve ser um número válido.'}), 400

    # 3. Validação de Integridade no Banco (FKs)
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        # Checar se as FKs existem
        tabelas_checar = [
            ("tipo_lancamento", tipo_id),
            ("categoria", cat_id),
            ("conta_corrente", conta_id)
        ]
        
        for tabela, id_val in tabelas_checar:
            cursor.execute(f"SELECT id FROM {tabela} WHERE id = ?", (id_val,))
            if not cursor.fetchone():
                return jsonify({'mensagem': f'O ID {id_val} não existe na tabela {tabela}.'}), 400

        # 4. Inserção Final
        sql = '''INSERT INTO lancamento 
                 (tipo_lancamento_id, data, valor, descricao, categoria_id, conta_corrente_id) 
                 VALUES (?, ?, ?, ?, ?, ?)'''
        
        cursor.execute(sql, (tipo_id, data_str, valor_float, descricao, cat_id, conta_id))
        connection.commit()
        
        return jsonify({'mensagem': 'Lançamento registrado!'}), 201

    except Exception as e:
        connection.rollback()
        return jsonify({'erro': str(e)}), 500
    finally:
        connection.close()