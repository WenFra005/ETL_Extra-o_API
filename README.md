# ETL_Extract_API

## Descrição
Projeto de ETL (Extract, Transform, Load) para extração de dados de uma API utilizando a biblioteca `requests` em Python. O objetivo é coletar dados de uma fonte externa, realizar possíveis transformações e armazenar os resultados para posterior análise ou integração.

## Funcionalidades
- Extração de dados de uma API REST
- Transformação básica dos dados (opcional)
- Armazenamento dos dados extraídos em arquivo ou banco de dados

## Requisitos
- Python 3.7+
- requests

### Instalação dos requisitos
```bash
pip install requests
```

## Estrutura do Projeto
```
ETL_Extracto_API/
├── etl.py           # Script principal de ETL
├── requirements.txt # Lista de dependências
├── README.md        # Documentação do projeto
```

## Exemplo de Uso
```python
import requests

url = 'https://api.exemplo.com/dados'
resposta = requests.get(url)
if resposta.status_code == 200:
    dados = resposta.json()
    # Transformação e armazenamento dos dados
else:
    print('Erro ao acessar a API:', resposta.status_code)
```

## Como Executar
1. Clone este repositório
2. Instale as dependências
3. Execute o script principal:
   ```bash
   python etl.py
   ```

## Licença
Este projeto está sob a licença MIT.