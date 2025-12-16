# Aplicação CRUD Simples com Python e MySQL

Aplicação Docker simples em Python (Flask) que realiza operações CRUD com MySQL.

## Como usar

### 1. Iniciar os serviços

```bash
docker-compose up -d
```

### 2. Acessar a API

A aplicação estará disponível em: `http://localhost:5000`

### 3. Endpoints disponíveis

- `GET /` - Informações sobre a API
- `GET /produtos` - Lista todos os produtos
- `GET /produtos/<id>` - Busca um produto por ID
- `POST /produtos` - Cria um novo produto
- `PUT /produtos/<id>` - Atualiza um produto
- `DELETE /produtos/<id>` - Deleta um produto

### 4. Exemplos de uso

#### Criar um produto:
```bash
curl -X POST http://localhost:5000/produtos \
  -H "Content-Type: application/json" \
  -d '{"nome": "Notebook", "preco": 2500.00, "descricao": "Notebook Dell"}'
```

#### Listar produtos:
```bash
curl http://localhost:5000/produtos
```

#### Buscar produto por ID:
```bash
curl http://localhost:5000/produtos/1
```

#### Atualizar produto:
```bash
curl -X PUT http://localhost:5000/produtos/1 \
  -H "Content-Type: application/json" \
  -d '{"nome": "Notebook Atualizado", "preco": 2300.00}'
```

#### Deletar produto:
```bash
curl -X DELETE http://localhost:5000/produtos/1
```

### 5. Parar os serviços

```bash
docker-compose down
```

Para remover também os volumes (dados do MySQL):
```bash
docker-compose down -v
```

