# Banco de Dados

O sistema utiliza o banco de dados PostgreSQL para armazenar de forma segura e estruturada as cotações do dólar.

## Modelo de Dados

A tabela principal é `dolar_data`, definida via SQLAlchemy ORM.

### Estrutura da Tabela

| Campo            | Tipo      | Descrição                        |
|------------------|-----------|----------------------------------|
| id               | Integer   | Chave primária                   |
| moeda_origem     | String(3) | Moeda de origem (ex: USD)        |
| moeda_destino    | String(3) | Moeda de destino (ex: BRL)       |
| valor_de_compra  | Float     | Valor de compra do dólar         |
| timestamp_moeda  | DateTime  | Data/hora da cotação             |
| timestamp_criacao| DateTime  | Data/hora de inserção no sistema |

## Exemplo de Query

```sql
-- Consulta das cotações mais recentes
SELECT * FROM dolar_data 
WHERE moeda_origem = 'USD' AND moeda_destino = 'BRL' 
ORDER BY timestamp_moeda DESC 
LIMIT 10;

-- Consulta por período
SELECT * FROM dolar_data 
WHERE timestamp_moeda >= '2024-05-01' 
AND timestamp_moeda <= '2024-05-31'
ORDER BY timestamp_moeda DESC;

-- Estatísticas básicas
SELECT 
    MIN(valor_de_compra) as preco_minimo,
    MAX(valor_de_compra) as preco_maximo,
    AVG(valor_de_compra) as preco_medio
FROM dolar_data 
WHERE moeda_origem = 'USD' AND moeda_destino = 'BRL';
```

## Configuração
- O modelo está definido em `src/database/database.py`
- A conexão é configurada em `src/config/config.py`
- As tabelas são criadas automaticamente pelo SQLAlchemy

## Observações
- O banco pode ser acessado por qualquer ferramenta compatível com PostgreSQL
- Novas tabelas podem ser adicionadas conforme a necessidade
- Os dados são inseridos automaticamente pelo pipeline ETL
- Backup regular é recomendado para dados de produção 