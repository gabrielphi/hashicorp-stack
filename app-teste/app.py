from flask import Flask, request, jsonify
import mysql.connector
import os
import time

app = Flask(__name__)

# Configuração do banco de dados
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'mysql'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'rootpassword'),
    'database': os.getenv('DB_NAME', 'testdb'),
    'port': int(os.getenv('DB_PORT', 3306))
}

def get_db_connection():
    """Estabelece conexão com o banco de dados"""
    max_retries = 5
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            return conn
        except mysql.connector.Error as e:
            retry_count += 1
            if retry_count >= max_retries:
                raise
            time.sleep(2)
    return None

def init_db():
    """Inicializa o banco de dados criando a tabela se não existir"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Criar tabela de produtos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                preco DECIMAL(10, 2) NOT NULL,
                descricao TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Banco de dados inicializado com sucesso!")
    except mysql.connector.Error as e:
        print(f"Erro ao inicializar banco de dados: {e}")

# Inicializar banco ao iniciar a aplicação
init_db()

@app.route('/')
def home():
    return jsonify({
        'message': 'API CRUD Simples',
        'endpoints': {
            'GET /produtos': 'Lista todos os produtos',
            'GET /produtos/<id>': 'Busca um produto por ID',
            'POST /produtos': 'Cria um novo produto',
            'PUT /produtos/<id>': 'Atualiza um produto',
            'DELETE /produtos/<id>': 'Deleta um produto'
        }
    })

@app.route('/produtos', methods=['GET'])
def listar_produtos():
    """Lista todos os produtos"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM produtos ORDER BY id DESC")
        produtos = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(produtos), 200
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/produtos/<int:id>', methods=['GET'])
def buscar_produto(id):
    """Busca um produto por ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM produtos WHERE id = %s", (id,))
        produto = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if produto:
            return jsonify(produto), 200
        else:
            return jsonify({'error': 'Produto não encontrado'}), 404
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/produtos', methods=['POST'])
def criar_produto():
    """Cria um novo produto"""
    try:
        data = request.get_json()
        
        if not data or 'nome' not in data or 'preco' not in data:
            return jsonify({'error': 'Nome e preço são obrigatórios'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO produtos (nome, preco, descricao)
            VALUES (%s, %s, %s)
        """, (data['nome'], data['preco'], data.get('descricao', '')))
        
        conn.commit()
        produto_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'message': 'Produto criado com sucesso',
            'id': produto_id
        }), 201
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    """Atualiza um produto existente"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar se o produto existe
        cursor.execute("SELECT id FROM produtos WHERE id = %s", (id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'error': 'Produto não encontrado'}), 404
        
        # Construir query de atualização dinamicamente
        updates = []
        values = []
        
        if 'nome' in data:
            updates.append("nome = %s")
            values.append(data['nome'])
        if 'preco' in data:
            updates.append("preco = %s")
            values.append(data['preco'])
        if 'descricao' in data:
            updates.append("descricao = %s")
            values.append(data['descricao'])
        
        if not updates:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Nenhum campo para atualizar'}), 400
        
        values.append(id)
        query = f"UPDATE produtos SET {', '.join(updates)} WHERE id = %s"
        
        cursor.execute(query, values)
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Produto atualizado com sucesso'}), 200
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/produtos/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    """Deleta um produto"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar se o produto existe
        cursor.execute("SELECT id FROM produtos WHERE id = %s", (id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'error': 'Produto não encontrado'}), 404
        
        cursor.execute("DELETE FROM produtos WHERE id = %s", (id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Produto deletado com sucesso'}), 200
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

