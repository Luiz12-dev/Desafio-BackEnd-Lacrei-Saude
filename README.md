# 🌈 Desafio Back-end – Lacrei Saúde

API RESTful de Gerenciamento de Consultas Médicas, desenvolvida como parte do desafio técnico da Lacrei Saúde. A aplicação é segura, escalável e pronta para produção, com foco em impacto social para a comunidade LGBTQIAPN+.

## 🚀 Tecnologias Utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python 3.12 | Linguagem principal |
| Django 6 + DRF | Framework web + API REST |
| Poetry | Gerenciamento de dependências |
| PostgreSQL 15 | Banco de dados relacional |
| Docker + Docker Compose | Containerização |
| GitHub Actions | CI/CD Pipeline |
| JWT (SimpleJWT) | Autenticação stateless |
| drf-spectacular | Documentação Swagger/Redoc |
| Gunicorn | Servidor WSGI para produção |
| WhiteNoise | Servir arquivos estáticos em produção |

---

## 🛠️ Setup do Ambiente

### Opção 1: Setup via Docker (Recomendado)

Para um ambiente replicável e de fácil execução.

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd lacrei-backend
   ```

2. **Suba os containers (Banco de Dados + Aplicação):**
   ```bash
   docker-compose up --build
   ```
   > O comando acima irá baixar a imagem do Postgres, buildar a imagem da API, rodar as migrações automaticamente e iniciar a aplicação na porta 8000.

3. **Crie um superusuário para obter o token JWT:**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

4. **Acesse a aplicação:**
   - API Root: `http://localhost:8000/api/`
   - Swagger UI: `http://localhost:8000/api/docs/swagger/`
   - Redoc: `http://localhost:8000/api/docs/redoc/`
   - Admin: `http://localhost:8000/admin/`

### Opção 2: Setup Local

1. **Pré-requisitos:**
   - Python 3.12+
   - Poetry instalado (`pip install poetry`)
   - PostgreSQL rodando localmente

2. **Instale as dependências:**
   ```bash
   poetry install
   ```

3. **Configure as variáveis de ambiente:**
   Crie um arquivo `.env` na raiz do projeto:
   ```env
   SECRET_KEY=minha-chave-secreta-de-desenvolvimento
   DEBUG=True
   ALLOWED_HOSTS=*
   DATABASE_URL=postgres://lacrei_user:lacrei_pass@localhost:5432/lacrei_db
   CORS_ALLOW_ALL_ORIGINS=True
   ```

4. **Execute as migrações:**
   ```bash
   poetry run python manage.py migrate
   ```

5. **Crie um superusuário:**
   ```bash
   poetry run python manage.py createsuperuser
   ```

6. **Rode o servidor:**
   ```bash
   poetry run python manage.py runserver
   ```

---

## 🔐 Autenticação (JWT)

A API utiliza autenticação via **JSON Web Token (JWT)**. Para acessar os endpoints protegidos:

1. **Obtenha o token:**
   ```bash
   curl -X POST http://localhost:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "seu_usuario", "password": "sua_senha"}'
   ```
   Resposta:
   ```json
   {
     "access": "eyJ0eXAiOiJKV1...",
     "refresh": "eyJ0eXAiOiJKV1..."
   }
   ```

2. **Use o token nas requisições:**
   ```bash
   curl -H "Authorization: Bearer <access_token>" \
     http://localhost:8000/api/profissionais/
   ```

3. **Renove o token quando expirar (válido por 60 minutos):**
   ```bash
   curl -X POST http://localhost:8000/api/token/refresh/ \
     -H "Content-Type: application/json" \
     -d '{"refresh": "seu_refresh_token"}'
   ```

---

## 📡 Endpoints da API

### Profissionais da Saúde

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/profissionais/` | Listar todos os profissionais |
| `POST` | `/api/profissionais/` | Cadastrar um novo profissional |
| `GET` | `/api/profissionais/{id}/` | Detalhar um profissional |
| `PUT` | `/api/profissionais/{id}/` | Atualizar um profissional (completo) |
| `PATCH` | `/api/profissionais/{id}/` | Atualizar parcialmente um profissional |
| `DELETE` | `/api/profissionais/{id}/` | Remover um profissional |
| `GET` | `/api/profissionais/{id}/consultas/` | Buscar consultas pelo ID do profissional |

### Consultas Médicas

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/consultas/` | Listar todas as consultas |
| `POST` | `/api/consultas/` | Agendar uma nova consulta |
| `GET` | `/api/consultas/{id}/` | Detalhar uma consulta |
| `PUT` | `/api/consultas/{id}/` | Atualizar uma consulta (completo) |
| `PATCH` | `/api/consultas/{id}/` | Atualizar parcialmente uma consulta |
| `DELETE` | `/api/consultas/{id}/` | Cancelar/remover uma consulta |

### Autenticação

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/api/token/` | Obter access + refresh token |
| `POST` | `/api/token/refresh/` | Renovar o access token |

### Documentação

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/docs/swagger/` | Swagger UI (interativo) |
| `GET` | `/api/docs/redoc/` | Redoc (referência) |
| `GET` | `/api/schema/` | Schema OpenAPI (JSON) |

---

## 🧪 Testes Automatizados

O projeto utiliza `APITestCase` do Django REST Framework, com **16 testes** organizados em duas suítes:

### Cobertura de Profissionais (`ProfissionalAPITestCase`):
- ✅ Criar profissional com dados válidos
- ✅ Listar profissionais
- ✅ Atualizar profissional (PATCH)
- ✅ Deletar profissional
- ✅ Rejeitar profissional sem nome (400)
- ✅ Rejeitar profissional com campos vazios (400)
- ✅ Bloquear tentativa de XSS (400)
- ✅ Rejeitar acesso sem autenticação (401)

### Cobertura de Consultas (`ConsultaAPITestCase`):
- ✅ Criar consulta com dados válidos
- ✅ Listar consultas
- ✅ Atualizar consulta (PATCH)
- ✅ Deletar consulta
- ✅ Buscar consultas por ID do profissional
- ✅ Rejeitar consulta com data no passado (400)
- ✅ Rejeitar consulta com profissional inexistente (400)
- ✅ Rejeitar acesso sem autenticação (401)

### Como rodar os testes:

```bash
# Setup local
poetry run python manage.py test --verbosity=2

# Via Docker
docker-compose exec web python manage.py test --verbosity=2
```

---

## ⚙️ Pipeline CI/CD (GitHub Actions)

O pipeline está em `.github/workflows/pipeline.yml` e é acionado em pushes para `main` e `staging`.

### Fluxo:

```
📥 Checkout → 🧹 Lint (Flake8) → 🧪 Testes (PostgreSQL) → 🏗️ Build Docker → 🚀 Deploy
```

| Etapa | Descrição |
|-------|-----------|
| **Lint** | `flake8` para verificar erros de sintaxe |
| **Testes** | `manage.py test` com serviço PostgreSQL 15 real |
| **Build** | Geração da imagem Docker da aplicação |
| **Deploy Staging** | Deploy automático ao pushar em `staging` |
| **Deploy Produção** | Deploy automático ao pushar em `main` |

### Ambientes:
- **Staging** → branch `staging` → Ambiente de homologação
- **Produção** → branch `main` → Ambiente final

---

## ☁️ Deploy (Staging e Produção)

O deploy utiliza separação de ambientes via branches do Git:

### Variáveis de ambiente para produção:

```env
SECRET_KEY=<chave-secreta-forte-e-aleatoria>
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com,api.seu-dominio.com
DATABASE_URL=postgres://usuario:senha@host:5432/nome_banco
CORS_ALLOWED_ORIGINS=https://seu-frontend.com
```

### Plataformas suportadas:
- **Render** (recomendado para MVP) — Deploy automático via GitHub
- **AWS ECS (Fargate)** — Para produção escalável com Blue/Green

---

## 🔄 Estratégia de Rollback

### Blue/Green Deployment (AWS)
- Manter dois ambientes em paralelo (Blue e Green)
- O deploy é feito na instância inativa (ex: Green)
- Após health checks, o ALB redireciona o tráfego para Green
- Em caso de falha: redirecionar o Load Balancer de volta ao Blue
- **Recuperação em segundos**, sem downtime

### Revert via GitHub Actions
- Utilizar `Revert Pull Request` no GitHub
- O CI é automaticamente acionado, gerando nova build e deploy da versão estável
- Ideal para emergências que demandam retorno imediato

---

## 🛡️ Segurança

| Medida | Implementação |
|--------|---------------|
| **SQL Injection** | Proteção nativa via ORM do Django (sem queries raw) |
| **XSS** | Sanitização nos serializers: detecção de `<script>`, `javascript:`, `onclick=`, `<iframe>`, etc. |
| **CORS** | `django-cors-headers` com lista de origens permitidas (`CORS_ALLOWED_ORIGINS`) |
| **Autenticação** | JWT via SimpleJWT — access token (60min) + refresh (24h) |
| **Validação** | Todos os campos validados nos serializers com mensagens claras em português |
| **Logs de acesso** | Middleware customizado registrando método, path, IP, status e tempo de resposta |
| **Logs de operações** | Registro de todas as criações, edições e exclusões nas views |
| **Secrets** | Variáveis sensíveis via `django-environ` (nunca hardcoded no código) |

---

## ⚙️ Decisões Técnicas

- **Django + DRF**: Ecossistema maduro para APIs REST, com ORM robusto que elimina riscos de SQL Injection, admin integrado e ampla comunidade de suporte.
- **Poetry**: Resolução determinística de dependências com `poetry.lock`, garantindo builds reproduzíveis entre ambientes.
- **UUID como Primary Key**: Evita enumeração sequencial de IDs, aumentando a segurança e adequação para sistemas distribuídos.
- **JWT (SimpleJWT)**: Autenticação stateless que favorece escalabilidade horizontal sem compartilhamento de sessão.
- **drf-spectacular**: Geração automática de documentação OpenAPI 3.0, com interfaces Swagger UI e Redoc.
- **Gunicorn**: Servidor WSGI de produção, multi-worker, substituindo o `runserver` do Django que não é adequado para produção.
- **WhiteNoise**: Serve arquivos estáticos diretamente da aplicação, sem necessidade de servidor proxy (Nginx) dedicado.
- **Middleware de Logs**: Registro granular de cada requisição HTTP para auditoria, debugging e monitoramento.
- **Sanitização em todos os campos**: Função utilitária reutilizável que detecta padrões maliciosos e remove tags HTML residuais.

---

## 💳 Proposta de Integração com Asaas (Split de Pagamento)

### Fluxo proposto:

1. **Onboarding**: Ao cadastrar o profissional, criar uma **Subconta no Asaas** (White-label) atrelando dados bancários.
2. **Split no Agendamento**: Ao gerar cobrança de consulta, enviar POST para API do Asaas com propriedade `split`:
   - Percentual retido pela Lacrei Saúde (taxa da plataforma)
   - Restante direcionado ao `walletId` da subconta do profissional
3. **Webhooks**: Endpoint escutando eventos do Asaas (ex: `PAYMENT_CONFIRMED`) para confirmar pagamento assíncrono e liberar a consulta.

---

## 📝 Erros Encontrados e Melhorias Propostas

### Erros corrigidos durante o desenvolvimento:
- **CORS aberto** (`CORS_ALLOW_ALL_ORIGINS=True`) — Corrigido para usar lista de origens permitidas via variável de ambiente.
- **Sanitização incompleta** — Inicialmente apenas `nome_social` e `contato` eram validados. Estendido para todos os campos com detecção de padrões maliciosos.
- **Pipeline sem PostgreSQL** — Os testes no CI não tinham banco de dados configurado. Adicionado serviço PostgreSQL 15 ao GitHub Actions.
- **Dockerfile com `runserver`** — Substituído por `gunicorn` para ambiente de produção.
- **Leitura do `.env` obrigatória** — Causava erro em ambientes sem o arquivo (Docker, CI). Corrigido para leitura condicional.

### Melhorias futuras:
- Adicionar paginação nos endpoints de listagem (`PageNumberPagination`)
- Implementar filtros avançados com `django-filter` (ex: buscar consultas por intervalo de data)
- Adicionar rate limiting para proteção contra abuso da API
- Implementar cache com Redis para consultas frequentes
- Adicionar testes de integração end-to-end
- Implementar soft delete (exclusão lógica) para preservar histórico
- Adicionar cobertura de testes com `coverage` e badge no README

---

💙 Agradeço a oportunidade de contribuir com a Lacrei Saúde!
