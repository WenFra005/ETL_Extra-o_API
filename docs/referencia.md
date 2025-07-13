# 📚 Referência da API Python

Esta página contém a documentação técnica completa de todas as funções, classes e módulos do projeto ETL Extract API.

## 🚀 Módulo Principal

### src.main
Módulo principal que executa o pipeline ETL de forma contínua com agendamento automático.

::: src.main

## 🔄 Pipeline ETL

### src.pipeline.extract
Responsável pela extração de dados de cotação do dólar de APIs externas.

::: src.pipeline.extract

### src.pipeline.transform  
Processa e valida os dados extraídos antes do carregamento.

::: src.pipeline.transform

### src.pipeline.load
Carrega os dados processados no banco de dados PostgreSQL.

::: src.pipeline.load

## 🗄️ Banco de Dados

### src.database.database
Modelos ORM e configurações de conexão com o banco de dados.

::: src.database.database

## 🔌 APIs Web

### src.api.health_api
Endpoints de health check para monitoramento do sistema.

::: src.api.health_api

### src.api.pipeline_web
Serviço web para execução do pipeline ETL via HTTP.

::: src.api.pipeline_web

## 📊 Dashboard

### src.dashboard.dashboard
Interface interativa para visualização dos dados de cotação.

::: src.dashboard.dashboard

---

💡 **Dica**: Use o menu lateral para navegar rapidamente entre as seções ou use Ctrl+F para buscar funções específicas.