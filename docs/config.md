# Configuração

A configuração do ETL Extract API é feita principalmente por variáveis de ambiente e arquivos de configuração Python.

## Variáveis de Ambiente

As principais variáveis necessárias são:

| Variável           | Descrição                                 |
|--------------------|-------------------------------------------|
| POSTGRES_USER      | Usuário do banco PostgreSQL               |
| POSTGRES_PASSWORD  | Senha do banco PostgreSQL                 |
| POSTGRES_HOST      | Host do banco PostgreSQL                  |
| POSTGRES_PORT      | Porta do banco PostgreSQL                 |
| POSTGRES_DB        | Nome do banco de dados                    |
| TOKEN_AWESOMEAPI   | Token de acesso à API de cotação          |

Exemplo de `.env`:
```env
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=etl_dolar
TOKEN_AWESOMEAPI=seu_token
```

## Arquivos de Configuração
- O arquivo `src/config/config.py` centraliza a leitura das variáveis de ambiente e configurações do sistema.
- O dashboard pode usar um arquivo `.streamlit/secrets.toml` para deploy no Streamlit Cloud.

## Deploy no Render

### Configuração do Pipeline
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn -w 1 -b 0.0.0.0:$PORT api.pipeline_web:app`
- **Health Check:** `/health-pipeline`

### Configuração do Dashboard
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `streamlit run src/dashboard/dashboard.py --server.port $PORT --server.address 0.0.0.0`
- **Health Check:** Automático pelo Streamlit

### Configuração do Health API
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn -w 1 -b 0.0.0.0:$PORT api.health_api:app`
- **Health Check:** `/health`

## Observações
- Nunca exponha suas credenciais em repositórios públicos.
- Use arquivos `.env` para facilitar o desenvolvimento local.
- No Render, configure as variáveis pelo painel web.
- O pipeline executa automaticamente em background quando deployado como serviço. 