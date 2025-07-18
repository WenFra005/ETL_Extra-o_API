"""
Módulo responsável pela transformação dos dados extraídos da cotação do dólar (USD-BRL).

Este módulo processa os dados brutos recebidos da API e os converte para o formato
padronizado usado internamente pelo sistema.
"""

from datetime import UTC, datetime
from zoneinfo import ZoneInfo


def transform_data(data):
    """Transforma os dados extraídos da API para o formato padronizado.

    Extrai informações relevantes dos dados brutos da API e as converte para
    o formato interno do sistema, incluindo conversão de timezone.

    Parameters
    ----------
    data : dict
        Dicionário contendo os dados extraídos da API com a chave "USDBRL".

    Returns
    -------
    dict
        Dicionário com os dados transformados contendo:
        - moeda_origem: Código da moeda de origem (USD)
        - moeda_destino: Código da moeda de destino (BRL)
        - valor_de_compra: Valor de compra do dólar em relação ao real
        - timestamp_moeda: Timestamp da cotação (timezone São Paulo)
        - timestamp_criacao: Timestamp de criação (timezone São Paulo)

    Examples
    --------
    >>> raw_data = {"USDBRL": {"code": "USD", "codein": "BRL", "bid": "5.12", "timestamp": "1640995200"}}
    >>> transformed = transform_data(raw_data)
    >>> print(transformed["valor_de_compra"])
    5.12
    """
    moeda_origem = data["USDBRL"]["code"]
    moeda_destino = data["USDBRL"]["codein"]
    valor_de_compra = data["USDBRL"]["bid"]
    timestamp_moeda = datetime.fromtimestamp(
        int(data["USDBRL"]["timestamp"]), tz=UTC
    ).astimezone(ZoneInfo("America/Sao_Paulo"))
    timestamp_criacao = datetime.now(UTC).astimezone(ZoneInfo("America/Sao_Paulo"))

    data_transformed = {
        "moeda_origem": moeda_origem,
        "moeda_destino": moeda_destino,
        "valor_de_compra": valor_de_compra,
        "timestamp_moeda": timestamp_moeda,
        "timestamp_criacao": timestamp_criacao,
    }

    return data_transformed


def transform_historical_data(data_list):
    """Transforma uma lista de cotações históricas da API para o formato padronizado.

    Parameters
    ----------
    data_list : list
        Lista de dicionários retornados pela API histórica.

    Returns
    -------
    list
        Lista de dicionários transformados prontos para inserção no banco.
    """
    from datetime import UTC, datetime
    from zoneinfo import ZoneInfo

    transformed = []
    # Pega code e codein do primeiro item (sempre tem)
    moeda_origem = data_list[0].get("code", "USD")
    moeda_destino = data_list[0].get("codein", "BRL")
    for data in data_list:
        valor_de_compra = data["bid"]
        timestamp_moeda = datetime.fromtimestamp(
            int(data["timestamp"]), tz=UTC
        ).astimezone(ZoneInfo("America/Sao_Paulo"))
        timestamp_criacao = datetime.now(UTC).astimezone(ZoneInfo("America/Sao_Paulo"))
        transformed.append(
            {
                "moeda_origem": data.get("code", moeda_origem),
                "moeda_destino": data.get("codein", moeda_destino),
                "valor_de_compra": valor_de_compra,
                "timestamp_moeda": timestamp_moeda,
                "timestamp_criacao": timestamp_criacao,
            }
        )
    return transformed
