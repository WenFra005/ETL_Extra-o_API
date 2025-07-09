from datetime import UTC, datetime
from zoneinfo import ZoneInfo

def transform_data(data):
    """
    Transforma os dados extraídos da API para o formato desejado. Extrai informações relevantes como
    moeda de origem, moeda de destino, valor de compra, timestamp da moeda e timestamp de criação.

    Parameters
    ----------
    data : dict
        Um dicionário contendo os dados extraídos da API, que deve conter a chave "USDBRL" com as
        informações da cotação do dólar em relação ao real brasileiro.

    Returns
    -------
    data_transformed : dict
        Um dicionário contendo os dados transformados, com as seguintes chaves:
        - moeda_origem: Código da moeda de origem (USD)
        - moeda_destino: Código da moeda de destino (BRL)
        - valor_de_compra: Valor de compra do dólar em relação ao real
        - timestamp_moeda: Timestamp da moeda convertido para o fuso horário de São Paulo
        - timestamp_criacao: Timestamp da criação do registro no fuso horário de São Paulo
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