from flask import Flask, request, jsonify, render_template_string
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
        
        # Criar tabela de pessoas (nome e idade)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pessoas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                idade INT NOT NULL,
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

# HTML template para a interface web
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cadastro de Pessoas</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            padding: 30px;
        }
        h1 {
            color: #333;
            margin-bottom: 30px;
            text-align: center;
        }
        .form-section {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #555;
            font-weight: 500;
        }
        input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            background: #667eea;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.3s;
        }
        button:hover {
            background: #5568d3;
        }
        .table-section {
            margin-top: 30px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background: #667eea;
            color: white;
            font-weight: 600;
        }
        tr:hover {
            background: #f8f9fa;
        }
        .message {
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 5px;
            display: none;
        }
        .message.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .message.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .empty-state {
            text-align: center;
            padding: 40px;
            color: #999;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📋 Cadastro de Pessoas</h1>
        
        <div id="message" class="message"></div>
        
        <div class="form-section">
            <h2 style="margin-bottom: 20px; color: #333;">Adicionar Nova Pessoa</h2>
            <form id="pessoaForm">
                <div class="form-group">
                    <label for="nome">Nome:</label>
                    <input type="text" id="nome" name="nome" required>
                </div>
                <div class="form-group">
                    <label for="idade">Idade:</label>
                    <input type="number" id="idade" name="idade" min="1" max="150" required>
                </div>
                <button type="submit">Adicionar</button>
            </form>
        </div>
        
        <div class="table-section">
            <h2 style="margin-bottom: 20px; color: #333;">Pessoas Cadastradas</h2>
            <div id="loading" style="text-align: center; padding: 20px;">Carregando...</div>
            <table id="pessoasTable" style="display: none;">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nome</th>
                        <th>Idade</th>
                    </tr>
                </thead>
                <tbody id="pessoasBody">
                </tbody>
            </table>
            <div id="emptyState" class="empty-state" style="display: none;">
                Nenhuma pessoa cadastrada ainda.
            </div>
        </div>
    </div>
    
    <script>
        // Carregar pessoas ao carregar a página
        window.addEventListener('DOMContentLoaded', carregarPessoas);
        
        // Submeter formulário
        document.getElementById('pessoaForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const nome = document.getElementById('nome').value;
            const idade = document.getElementById('idade').value;
            
            try {
                const response = await fetch('/api/pessoas', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ nome, idade: parseInt(idade) })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    mostrarMensagem('Pessoa adicionada com sucesso!', 'success');
                    document.getElementById('pessoaForm').reset();
                    carregarPessoas();
                } else {
                    mostrarMensagem('Erro: ' + data.error, 'error');
                }
            } catch (error) {
                mostrarMensagem('Erro ao adicionar pessoa: ' + error.message, 'error');
            }
        });
        
        async function carregarPessoas() {
            try {
                const response = await fetch('/api/pessoas');
                const pessoas = await response.json();
                
                document.getElementById('loading').style.display = 'none';
                
                const tbody = document.getElementById('pessoasBody');
                tbody.innerHTML = '';
                
                if (pessoas.length === 0) {
                    document.getElementById('pessoasTable').style.display = 'none';
                    document.getElementById('emptyState').style.display = 'block';
                } else {
                    document.getElementById('pessoasTable').style.display = 'table';
                    document.getElementById('emptyState').style.display = 'none';
                    
                    pessoas.forEach(pessoa => {
                        const tr = document.createElement('tr');
                        tr.innerHTML = `
                            <td>${pessoa.id}</td>
                            <td>${pessoa.nome}</td>
                            <td>${pessoa.idade}</td>
                        `;
                        tbody.appendChild(tr);
                    });
                }
            } catch (error) {
                document.getElementById('loading').textContent = 'Erro ao carregar pessoas';
                mostrarMensagem('Erro ao carregar pessoas: ' + error.message, 'error');
            }
        }
        
        function mostrarMensagem(texto, tipo) {
            const messageDiv = document.getElementById('message');
            messageDiv.textContent = texto;
            messageDiv.className = 'message ' + tipo;
            messageDiv.style.display = 'block';
            
            setTimeout(() => {
                messageDiv.style.display = 'none';
            }, 3000);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Página principal com interface web"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/pessoas', methods=['GET'])
def listar_pessoas():
    """Lista todas as pessoas"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT id, nome, idade FROM pessoas ORDER BY id DESC")
        pessoas = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(pessoas), 200
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pessoas', methods=['POST'])
def criar_pessoa():
    """Cria uma nova pessoa"""
    try:
        data = request.get_json()
        
        if not data or 'nome' not in data or 'idade' not in data:
            return jsonify({'error': 'Nome e idade são obrigatórios'}), 400
        
        nome = data['nome'].strip()
        idade = int(data['idade'])
        
        if not nome:
            return jsonify({'error': 'Nome não pode estar vazio'}), 400
        
        if idade < 1 or idade > 150:
            return jsonify({'error': 'Idade deve estar entre 1 e 150'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO pessoas (nome, idade)
            VALUES (%s, %s)
        """, (nome, idade))
        
        conn.commit()
        pessoa_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'message': 'Pessoa criada com sucesso',
            'id': pessoa_id
        }), 201
    except ValueError:
        return jsonify({'error': 'Idade deve ser um número válido'}), 400
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

