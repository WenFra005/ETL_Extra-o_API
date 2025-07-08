"""
Este módulo implementa um pipeline de dados que extrai, transforma e salva dados da cotação
do dólar em relação ao real brasileiro (USD-BRL) em um banco de dados PostgreSQL.
"""

import signal
import threading
import time
from datetime import UTC, datetime
from venv import logger
from zoneinfo import ZoneInfo

import logfire
import requests
from flask import app

from config import TOKEN_AWESOMEAPI, configure_ambient_logging, configure_database
from database import Base, DolarData
from health_api import handle_sigterm


def create_tables(engine, logger):
    """
    Cria as tabelas no banco de dados PostgreSQL usando SQLAlchemy. Utiliza o objeto engine para
    interagir com o banco de dados e cria as tabelas definidas no modelo Base.

    Parameters
    ----------
    engine : sqlalchemy.engine.Engine
        Um objeto engine do SQLAlchemy configurado para se conectar ao banco de dados PostgreSQL.

    logger : logging.Logger
        Um objeto logger configurado para registrar logs do pipeline de dados.
    """
    Base.metadata.create_all(engine)
    logger.info("Tabelas criadas/verificadas com sucesso.")


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


def save_data_postgres(Session, data, logger):
    """
    Salva os dados transformados no banco de dados PostgreSQL. Utiliza uma sessão do SQLAlchemy para
    adicionar um novo registro na tabela DolarData. Se ocorrer um erro, a transação é revertida.

    Parameters
    ----------
    Session : sqlalchemy.orm.session.Session
        Uma classe de sessão do SQLAlchemy para interagir com o banco de dados.

    data : dict
        Um dicionário contendo os dados transformados, que deve conter as chaves:
        - moeda_origem
        - moeda_destino
        - valor_de_compra
        - timestamp_moeda
        - timestamp_criacao
    logger : logging.Logger
        Um objeto logger configurado para registrar logs do pipeline de dados.
    """
    session = Session()
    try:
        novo_registro = DolarData(**data)
        session.add(novo_registro)
        session.commit()
        logger.info(
            f"[{data['timestamp_criacao'].strftime('%d/%m/%y %H:%M:%S')}] "
            f"Dados salvos com sucesso no banco de dados PostgreSQL."
        )
    except Exception as e:
        logger.error(f"Erro ao salvar dados no PostgreSQL: {e}")
        session.rollback()
    finally:
        session.close()


def pipeline(Session, logger):
    """
    Executa o pipeline de dados, que consiste em extrair, transformar e salvar os dados
    no banco de dados PostgreSQL.

    Parameters
    ----------
    Session : sqlalchemy.orm.session.Session
        Uma classe de sessão do SQLAlchemy para interagir com o banco de dados.

    logger : logging.Logger
        Um objeto logger configurado para registrar logs do pipeline de dados.
    """
    with logfire.span("Extraindo dados"):
        data = extract_data(logger)

    if not data:
        logger.error("Nenhum dado foi extraído. Encerrando o pipeline.")
        return

    with logfire.span("Transformando dados"):
        transformed_data = transform_data(data)

    with logfire.span("Salvando dados no PostgreSQL"):
        save_data_postgres(Session, transformed_data, logger)

    logger.info("Pipeline de dados concluído com sucesso.")


def loop_pipeline(Session, logger):
    """
    Executa o pipeline de dados em um loop contínuo, com intervalos de espera entre as execuções.

    Parameters
    ----------
    Session : sqlalchemy.orm.session.Session
        Uma classe de sessão do SQLAlchemy para interagir com o banco de dados.
    logger : logging.Logger
        Um objeto logger configurado para registrar logs do pipeline de dados.
    """
    while True:
        with logfire.span("Executando o pipeline"):
            try:
                pipeline(Session, logger)
                logger.info("Aguardando 30 segundos para a próxima execução...")
                time.sleep(30)
            except KeyboardInterrupt:
                logger.info("Pipeline interrompido pelo usuário.")
                break
            except Exception as e:
                logger.error(f"Ocorreu um erro inesperado: {e}")
                time.sleep(30)
        logger.info("Pipeline finalizado.")
    logger.info("Execução encerrada.")


if __name__ == "__main__":
    logger = configure_ambient_logging()
    signal.signal(signal.SIGTERM, handle_sigterm)
    engine, Session = configure_database()
    create_tables(engine, logger)
    logger.info("Iniciando...")

    threading.Thread(target=loop_pipeline, args=(Session, logger)).start()
    app.run(host="0.0.0.0", port=10000)
