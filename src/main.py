"""
Módulo principal para execução do pipeline ETL de cotação do dólar (USD-BRL).
Este script inicializa o ambiente, cria as tabelas e executa o pipeline de extração, transformação
e carga.
"""

import datetime
import signal
import threading
import time

import logfire

from src.config.config import configure_ambient_logging, configure_database
from src.database.database import Base
from src.pipeline.extract import extract_data
from src.pipeline.load import save_data_postgres
from src.pipeline.transform import transform_data

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


def is_within_allowed_time():
    """
    Verifica se o horário atual está dentro do intervalo permitido para a execução do pipeline.
    O intervalo permitido é das 08:00 às 19:00 (horário local).

    Returns
    -------
    bool
        Retorna True se o horário atual estiver dentro do intervalo permitido, caso contrário, retorna False.
    """
    now = datetime.datetime.now()
    start = now.replace(hour=8, minute=0, second=0, microsecond=0)
    end = now.replace(hour=19, minute=0, second=0, microsecond=0)
    return start <= now <= end


def time_until_next_start():
    """
    Calcula o tempo restante até o próximo início permitido do pipeline, que é às 08:00
    do dia seguinte.
    Se o horário atual já for após as 08:00, o próximo início será no dia seguinte às 08:00.

    Returns
    -------
    datetime.timedelta
        Um objeto timedelta representando o tempo restante até o próximo início permitido do
        pipeline.
    """
    now = datetime.datetime.now()
    next_start = now.replace(hour=8, minute=0, second=0, microsecond=0)
    if now >= next_start:
        next_start = next_start + datetime.timedelta(days=1)
    return next_start - now


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
        if is_within_allowed_time():
            with logfire.span("Executando o pipeline"):
                try:
                    pipeline(Session, logger)
                    logger.info("Aguardando 30 segundos para a próxima execução...")
                    stop_event.wait(30)
                except Exception as e:
                    logger.error(f"Ocorreu um erro inesperado: {e}")
                    time.sleep(30)
            logger.info("Pipeline finalizado.")
        else:
            time_remaining = time_until_next_start()
            minutes, seconds = divmod(time_remaining.seconds, 60)
            hours, minutes = divmod(minutes, 60)
            logger.info(
                f"Fora do horário permitido (08:00-19:00). Tempo restante até o próximo início: {hours:02d}:{minutes:02d}:{seconds:02d}. Checando novamente em 10 minutos..."
            )
            stop_event.wait(600)  # 10 minutos
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
