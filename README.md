# ETL Extract API - Sistema de Monitoramento de Cotação do Dólar

## 🎥 Demonstração

![Demonstração do Projeto](assets/demo.gif)

## 📊 Sobre o Projeto

O **ETL Extract API** é um sistema completo de monitoramento e análise de dados de cotação do dólar (USD-BRL) em tempo real, criado como exercício prático de conceitos de ETL, API REST, dashboard interativo e integração com banco de dados. O objetivo principal é servir como referência didática para quem deseja aprender sobre esses temas na prática.

## 🎯 O que este projeto faz?

### 🔄 Pipeline ETL Automatizado
- **Extração**: Coleta dados de cotação do dólar de APIs confiáveis
- **Transformação**: Processa e valida os dados recebidos
- **Carga**: Armazena os dados em banco PostgreSQL para análise histórica
- **Agendamento**: Executa automaticamente em horários específicos (08:00-19:00, dias úteis)

### 📈 Dashboard Interativo
- Visualização em tempo real da evolução da cotação
- Filtros por período (hora, dia, semana, mês)
- Gráficos interativos e métricas estatísticas
- Interface responsiva e intuitiva

### 🔌 API REST
- Health check para monitoramento do sistema
- Endpoints de status dos serviços

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.10+** - Linguagem principal
- **Flask** - Framework web para APIs
- **SQLAlchemy** - ORM para banco de dados
- **PostgreSQL** - Banco de dados relacional
- **Pandas** - Manipulação e análise de dados
- **Logfire** - Sistema de logging estruturado

### Frontend
- **Streamlit** - Dashboard interativo

### Infraestrutura
- **Render** - Plataforma de deploy na nuvem
- **Gunicorn** - Servidor WSGI para produção
- **GitHub** - Controle de versão

## 🚀 Qual é a utilidade deste projeto?

Este projeto é voltado para fins de estudo e demonstração. Ele pode ser útil para:

- **Estudantes e desenvolvedores** que queiram entender na prática como construir um pipeline ETL, expor dados via API, criar dashboards com Streamlit e integrar com banco de dados.
- **Exemplos de arquitetura** para projetos de dados.
- **Exploração de integração com APIs externas** e automação de processos de dados.

> **Não recomendado para uso em produção ou aplicações críticas.**

## 📁 Estrutura do Projeto

```
ETL_Extract_API/
├── src/
│   ├── api/                 # Endpoints da API REST
│   │   ├── health_api.py    # Health check
│   │   └── pipeline_web.py  # Pipeline como web service
│   ├── dashboard/           # Interface de visualização
│   │   └── dashboard.py     # Dashboard Streamlit
│   ├── pipeline/            # Pipeline ETL
│   │   ├── extract.py       # Extração de dados
│   │   ├── transform.py     # Transformação
│   │   └── load.py          # Carga no banco
│   ├── database/            # Camada de dados
│   │   └── database.py      # Modelos ORM
│   ├── config/              # Configurações
│   │   └── config.py        # Variáveis de ambiente
│   └── main.py              # Execução local do pipeline
├── docs/                    # Documentação MkDocs
├── requirements.txt         # Dependências Python
└── README.md               # Esta documentação
```

## 🔧 Instalação e Configuração

### Pré-requisitos
- Python 3.10+
- PostgreSQL
- Conta na AwesomeAPI (para dados de cotação)

### Instalação Local
```bash
# Clone o repositório
git clone https://github.com/WenFra005/ETL_Extract_API.git
cd ETL_Extract_API

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas credenciais
```

### Variáveis de Ambiente
```bash
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=etl_dolar
TOKEN_AWESOMEAPI=seu_token
```

### 🔗 Links Úteis da AwesomeAPI
- [Documentação da AwesomeAPI - Cotações](https://docs.awesomeapi.com.br/api-de-moedas)
- [Cadastro para obter token gratuito](https://awesomeapi.com.br/)

## 🚀 Como Executar

### Execução Local
```bash
# Pipeline ETL (execução contínua)
python src/main.py

# Dashboard (interface web)
streamlit run src/dashboard/dashboard.py

# API de health check
python src/api/health_api.py

# Pipeline como web service
python src/api/pipeline_web.py
```

### Deploy na Nuvem (Render)
O projeto está configurado para deploy automático no Render (utilizando o plano gratuito) com:
- Dashboard público para visualização
- Pipeline executando em background
- Health check para monitoramento

## 📊 Funcionalidades Principais

### Dashboard
- ✅ Visualização em tempo real
- ✅ Filtros por período (hora, dia, semana, mês)
- ✅ Gráficos interativos
- ✅ Métricas estatísticas
- ✅ Interface responsiva

### Pipeline ETL
- ✅ Extração automática
- ✅ Validação de dados
- ✅ Armazenamento histórico
- ✅ Execução agendada (08:00-19:00, dias úteis)
- ✅ Logs estruturados
- ✅ Controle de horário e dias da semana

### API
- ✅ Health check (`/health`)
- ✅ Status do pipeline (`/health-pipeline`)
- ✅ Documentação automática

## 🔍 Monitoramento e Logs

O sistema inclui:
- **Logs estruturados** com Logfire
- **Health check** para monitoramento
- **Métricas de performance**
- **Tratamento de erros**
- **Controle de execução por horário**

## 📖 Documentação

### 📚 Documentação Online
- **Site da documentação**: [ETL Extract API Docs](https://wenfra005.github.io/ETL_Extract_API/)
- **Referência da API**: Documentação automática das funções e classes

### 🔧 Documentação Local
- **Pasta `/docs`**: Documentação técnica completa
- **README.md**: Este arquivo - guia rápido de início
- **Geração local**: Execute `mkdocs serve` para visualizar localmente

### 📋 Páginas Disponíveis
- **[Visão Geral](docs/index.md)** - Introdução e arquitetura
- **[API](docs/api.md)** - Endpoints de health check
- **[Pipeline ETL](docs/pipeline.md)** - Fluxo de dados
- **[Dashboard](docs/dashboard.md)** - Interface de visualização
- **[Banco de Dados](docs/database.md)** - Modelos e estrutura
- **[Configuração](docs/config.md)** - Setup e variáveis
- **[Referência](docs/referencia.md)** - Documentação técnica automática

## 🤝 Contribuição

Este projeto não é mantido ativamente, mas contribuições, sugestões ou correções são bem-vindas para fins de aprendizado coletivo!

1. Fork o projeto (opcional)
2. Crie uma branch para sua feature ou ajuste
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença [MIT](LICENSE).

## 📞 Suporte

Para dúvidas ou suporte:
- Abra uma [issue](https://github.com/WenFra005/ETL_Extract_API/issues)
- Consulte a [documentação online](https://wenfra005.github.io/ETL_Extract_API/)
- Entre em contato através do GitHub

