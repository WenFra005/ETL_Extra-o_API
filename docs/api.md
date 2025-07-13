# API

A API do ETL Extract API permite verificar a saúde dos serviços e monitorar o status do sistema.

## Endpoints Disponíveis

### `/health`
- **Método:** GET
- **Descrição:** Verifica se o serviço de health check está online.
- **Resposta:**
```json
{
  "status": "ok"
}
```

### `/health-pipeline`
- **Método:** GET
- **Descrição:** Verifica se o serviço de pipeline está online e funcionando.
- **Resposta:**
```json
{
  "status": "ok"
}
```

## Exemplos de Uso

```bash
# Health check do serviço principal
curl https://seuservico.onrender.com/health

# Health check do pipeline
curl https://seuservico.onrender.com/health-pipeline
```

## Observações
- Todos os endpoints retornam JSON.
- Os health checks podem ser usados para monitoramento automático.
- O pipeline executa automaticamente em background conforme agendamento configurado.
- Não há endpoints para execução manual do pipeline ou consulta de dados. 