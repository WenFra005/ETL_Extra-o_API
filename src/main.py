"""
Módulo principal para execução do pipeline ETL de cotação do dólar (USD-BRL).
Este script inicializa o ambiente, cria as tabelas e executa o pipeline de extração, transformação
e carga.
"""

import signal
import sys
import threading
import time

import logfire

from config.config import configure_ambient_logging, configure_database
from database.database import Base
from pipeline.extract import extract_data
from pipeline.load import save_data_postgres
from pipeline.transform import transform_data

stop_event = threading.Event()


def handle_sigterm(_signum, _frame):
    """
    Gerencia o sinal de término (SIGTERM) para encerrar o pipeline.

    Parameters
    ----------
    _signum : int
        O número do sinal recebido.
    _frame : frame
        O frame atual do programa.
    """
    logger.info("Recebido sinal de término (SIGTERM). Encerrando o pipeline...")
    stop_event.set()
    sys.exit(0)


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
    while not stop_event.is_set():
        with logfire.span("Executando o pipeline"):
            try:
                pipeline(Session, logger)
                logger.info("Aguardando 30 segundos para a próxima execução...")
                stop_event.wait(30)
            except Exception as e:
                logger.error(f"Ocorreu um erro inesperado: {e}")
                time.sleep(30)
        logger.info("Pipeline finalizado.")
    logger.info("Execução encerrada.")


if __name__ == "__main__":
    # Este bloco permite rodar o pipeline ETL localmente, sem necessidade de servidor web (Flask).
    # Use este arquivo para testes, execução manual ou scripts locais.
    logger = configure_ambient_logging()
    signal.signal(signal.SIGTERM, handle_sigterm)
    engine, Session = configure_database()
    create_tables(engine, logger)
    logger.info("Iniciando...")

    pipeline_thread = threading.Thread(target=loop_pipeline, args=(Session, logger))
    pipeline_thread.start()
    try:
        while pipeline_thread.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Interrupção do teclado recebida. Encerrando o pipeline...")
        stop_event.set()
        pipeline_thread.join()
