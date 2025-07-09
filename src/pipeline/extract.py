"""
Módulo responsável pela extração de dados da cotação do dólar (USD-BRL) via API.
"""

import requests

from src.config.config import TOKEN_AWESOMEAPI


def extract_data(logger):
    """
    Extrai dados da API AwesomeAPI para obter a cotação do dólar em relação
    ao real brasileiro (USD-BRL).

    Parameters
    ----------
    logger : logging.Logger
        Um objeto logger configurado para registrar logs do pipeline de dados.

    Returns
    -------
    data : dict or None
        Um dicionário contendo os dados extraídos da API, ou None se houver um erro na requisição.
    """
    url = (
        f"https://economia.awesomeapi.com.br/json/last/USD-BRL?token={TOKEN_AWESOMEAPI}"
    )
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Erro ao acessar a API: {response.status_code} - {response.text}")
        return None
