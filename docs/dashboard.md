# Dashboard

O dashboard do ETL Extract API permite visualizar e analisar a cotação do dólar de forma interativa e intuitiva.

## Funcionalidades
- Visualização em tempo real dos dados de cotação
- Filtros de período: hora, dia, semana, mês, todos os dados
- Gráfico de linha da evolução do dólar
- Tabela de dados recentes
- Métricas estatísticas: preço atual, máximo, mínimo

## Como acessar
- O dashboard pode ser acessado via navegador, em um link público (ex: Render ou Streamlit Cloud)
- Exemplo: `https://seuprojeto.onrender.com`

## Filtros de Período
- **Última Hora**: Mostra apenas as cotações da última hora
- **Último Dia**: Mostra as cotações das últimas 24 horas
- **Última Semana**: Mostra os dados dos últimos 7 dias
- **Último Mês**: Mostra os dados dos últimos 30 dias
- **Todos os Dados**: Mostra todo o histórico disponível

## Interface Interativa
- **Botões de zoom** organizados horizontalmente
- **Estado persistente** - O período selecionado é mantido
- **Atualização dinâmica** - Tabela, gráfico e métricas são atualizados automaticamente
- **Indicador visual** - Mostra qual período está ativo

## Gráficos e Tabelas
- O gráfico de linha mostra a evolução do valor de compra do dólar ao longo do tempo
- A tabela exibe os dados brutos mais recentes
- As métricas mostram o preço atual, máximo e mínimo do período selecionado

## Observações
- O dashboard é atualizado automaticamente conforme novos dados são inseridos
- Não é necessário login para acessar (padrão público)
- Pode ser customizado para outros tipos de visualização
- Execução via `streamlit run src/dashboard/dashboard.py` 