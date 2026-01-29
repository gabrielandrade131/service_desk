API Service Desk

Uma API REST para gerenciar tickets de suporte. Desenvolvida com Flask e MySQL.

INSTALACAO

1 - Entre na pasta
cd c:/service_desk

2 - Crie o ambiente virtual
python -m venv venv

3 - Ative o ambiente
Windows:
venv\Scripts\activate

Linux/Mac:
source venv/bin/activate

4 - Instale as dependências
pip install -r requirements.txt

5 - Configure o .env
DB_HOST=localhost
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=service_desk

6 - Crie o banco


ENDPOINTS

GET /api/health

TICKETS
GET /api/tickets
GET /api/tickets/1
POST /api/tickets
PUT /api/tickets/1
DELETE /api/tickets/1

USUARIOS
GET /api/usuarios
GET /api/usuarios/1
POST /api/usuarios
PUT /api/usuarios/1
DELETE /api/usuarios/1

SETORES
GET /api/setores
GET /api/setores/1
POST /api/setores
PUT /api/setores/1
DELETE /api/setores/1


EXEMPLOS

Listar tickets:
curl http://localhost:5000/api/tickets

Criar ticket:
curl -X POST http://localhost:5000/api/tickets \
  -H "Content-Type: application/json" \
  -d '{"titulo":"WiFi offline","descricao":"Sem internet","usuarios_id":1,"setores_id":1}'

Atualizar ticket:
curl -X PUT http://localhost:5000/api/tickets/1 \
  -H "Content-Type: application/json" \
  -d '{"status":"Em Atendimento"}'

Deletar ticket:
curl -X DELETE http://localhost:5000/api/tickets/1


ARQUIVOS PRINCIPAIS

app.py - Arquivo principal
config.py - Configurações do banco
models.py - Modelos das tabelas
routes/ - Endpoints
  tickets.py
  usuarios.py
  setores.py
requirements.txt - Dependências
.env - Variáveis de ambiente
.gitignore - Arquivos ignorados
