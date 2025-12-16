# Aplicação CRUD Simples com Python e MySQL

Aplicação Docker simples em Python (Flask) com interface web para cadastro de pessoas (nome e idade).

## Como usar

### 1. Iniciar os serviços

```bash
docker-compose up -d
```

### 2. Acessar a aplicação

Abra seu navegador e acesse: `http://localhost:5000`

A interface web permite:
- Visualizar todas as pessoas cadastradas
- Adicionar novas pessoas (nome e idade)

### 3. API REST (opcional)

A aplicação também expõe uma API REST:

- `GET /api/pessoas` - Lista todas as pessoas
- `POST /api/pessoas` - Cria uma nova pessoa

#### Exemplo de uso da API:

```bash
# Criar uma pessoa
curl -X POST http://localhost:5000/api/pessoas \
  -H "Content-Type: application/json" \
  -d '{"nome": "João Silva", "idade": 30}'

# Listar pessoas
curl http://localhost:5000/api/pessoas
```

### 4. Parar os serviços

```bash
docker-compose down
```

Para remover também os volumes (dados do MySQL):
```bash
docker-compose down -v
```

