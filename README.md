# ETL Extract API - Sistema de Monitoramento de Cotação do Dólar

## 📊 Sobre o Projeto

O **ETL Extract API** é um sistema completo de monitoramento e análise de dados de cotação do dólar (USD-BRL) em tempo real. Este projeto implementa um pipeline ETL (Extract, Transform, Load) automatizado que coleta dados de APIs externas, processa as informações e disponibiliza visualizações interativas através de um dashboard moderno.

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
- Endpoints para consulta de dados históricos
- Health check para monitoramento do sistema
- Execução manual do pipeline via web

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.10+** - Linguagem principal
- **FastAPI/Flask** - Framework web para APIs
- **SQLAlchemy** - ORM para banco de dados
- **PostgreSQL** - Banco de dados relacional
- **Pandas** - Manipulação e análise de dados
- **Logfire** - Sistema de logging estruturado

### Frontend
- **Streamlit** - Dashboard interativo
- **HTML/CSS** - Interface web

### Infraestrutura
- **Render** - Plataforma de deploy na nuvem
- **Gunicorn** - Servidor WSGI para produção
- **GitHub** - Controle de versão

## 🚀 Qual é a utilidade deste projeto?

### Para Investidores e Traders
- **Monitoramento em tempo real** da cotação do dólar
- **Análise histórica** para tomada de decisões
- **Alertas visuais** sobre tendências de mercado
- **Dados confiáveis** para estratégias de investimento

### Para Desenvolvedores
- **Exemplo prático** de implementação de pipeline ETL
- **Arquitetura escalável** para projetos de dados
- **Integração com APIs** externas
- **Deploy automatizado** na nuvem

### Para Empresas
- **Monitoramento de risco cambial**
- **Dados para relatórios financeiros**
- **Base para sistemas de trading automatizado**
- **Análise de impacto econômico**

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
├── requirements.txt         # Dependências Python
├── production_checklist.md  # Checklist para produção
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
O projeto está configurado para deploy automático no Render com:
- Dashboard público para visualização
- Pipeline executando em background
- Health check para monitoramento

## 📊 Funcionalidades Principais

### Dashboard
- ✅ Visualização em tempo real
- ✅ Filtros por período
- ✅ Gráficos interativos
- ✅ Métricas estatísticas
- ✅ Interface responsiva

### Pipeline ETL
- ✅ Extração automática
- ✅ Validação de dados
- ✅ Armazenamento histórico
- ✅ Execução agendada
- ✅ Logs estruturados

### API
- ✅ Endpoints REST
- ✅ Health check
- ✅ Execução manual
- ✅ Documentação automática

## 🔍 Monitoramento e Logs

O sistema inclui:
- **Logs estruturados** com Logfire
- **Health check** para monitoramento
- **Métricas de performance**
- **Tratamento de erros**

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença [MIT](LICENSE).

## 📞 Suporte

Para dúvidas ou suporte:
- Abra uma [issue](https://github.com/WenFra005/ETL_Extract_API/issues)
- Entre em contato através do GitHub

