# ETL Extract API - Cotação do Dólar (USD-BRL)

Este projeto implementa um pipeline ETL para extrair, transformar e carregar dados da cotação do dólar (USD-BRL) em um banco de dados PostgreSQL, além de fornecer um dashboard interativo e endpoints de health check.

## Estrutura do Projeto

```text
ETL_Extract_API/
├── requirements.txt         # Lista de dependências do projeto
├── README.md                # Documentação do projeto
└── src/
    ├── main.py              # Execução local do pipeline ETL (não web)
    ├── api/
    │   ├── pipeline_web.py  # Pipeline como Web Service (Flask + Gunicorn para Render)
    │   └── health_api.py    # Endpoint de health check (Flask)
    ├── dashboard/
    │   └── dashboard.py     # Dashboard interativo com Streamlit
    ├── pipeline/
    │   ├── extract.py       # Módulo de extração de dados da API
    │   ├── transform.py     # Módulo de transformação dos dados extraídos
    │   └── load.py          # Módulo de carga dos dados no banco de dados
    ├── database/
    │   └── database.py      # Definição do modelo ORM (SQLAlchemy) para a tabela do dólar
    └── config/
        └── config.py        # Configuração de ambiente e conexão com o banco
```

## Requisitos

- Python 3.10+
- PostgreSQL
- Variáveis de ambiente configuradas (ver abaixo)

## Instalação

```sh
pip install -r requirements.txt
```

## Variáveis de Ambiente

Configure as seguintes variáveis no Render (ou em um arquivo `.env` para uso local):

```
POSTGRES_USER=...
POSTGRES_PASSWORD=...
POSTGRES_HOST=...
POSTGRES_PORT=...
POSTGRES_DB=...
TOKEN_AWESOMEAPI=...
```

## Como Executar

### Localmente

#### Pipeline ETL (execução local)
```sh
python src/main.py
```

#### Dashboard (Streamlit)
```sh
streamlit run src/dashboard/dashboard.py
```

#### Health Check (Flask)
```sh
python src/api/health_api.py
```

#### Pipeline como Web Service (Flask)
```sh
python src/api/pipeline_web.py
```

### Produção (Render)

#### 1. Deploy do código no GitHub/GitLab

#### 2. Crie dois Web Services gratuitos no Render:

##### Dashboard
- **Build Command:**
  ```
  pip install -r requirements.txt
  ```
- **Start Command:**
  ```
  streamlit run src/dashboard/dashboard.py --server.port $PORT --server.address 0.0.0.0
  ```

##### Pipeline
- **Build Command:**
  ```
  pip install -r requirements.txt
  ```
- **Start Command:**
  ```
  gunicorn -w 1 -b 0.0.0.0:$PORT api.pipeline_web:app
  ```

##### (Opcional) Health API
- **Start Command:**
  ```
  gunicorn -w 1 -b 0.0.0.0:$PORT api.health_api:app
  ```

#### 3. Configure as variáveis de ambiente no painel do Render

#### 4. (Opcional) Use um arquivo `render.yaml` para automatizar o deploy

```
services:
  - type: web
    name: dashboard
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run src/dashboard/dashboard.py --server.port $PORT --server.address 0.0.0.0
    plan: free

  - type: web
    name: pipeline
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn -w 1 -b 0.0.0.0:$PORT api.pipeline_web:app
    plan: free
```

## Observações
- O pipeline é executado em background via thread no serviço Flask.
- O Gunicorn é usado para produção, conforme recomendado pela documentação do Flask.
- O dashboard e o pipeline podem ser acessados por URLs diferentes fornecidas pelo Render.

## Licença

Este projeto está sob a licença [MIT](LICENSE)
