"""
Módulo principal para execução do pipeline ETL de cotação do dólar (USD-BRL).

Este script inicializa o ambiente, cria as tabelas e executa o pipeline de extração,
transformação e carga de dados de cotação do dólar.

O pipeline executa automaticamente em horários específicos (08:00-19:00, dias úteis)
e pode ser interrompido via SIGTERM ou Ctrl+C.
"""

import datetime
import signal
import threading
import time
from zoneinfo import ZoneInfo

import logfire

from src.config.config import configure_ambient_logging, configure_database
from src.database.database import Base, DolarData
from src.pipeline.extract import extract_data, extract_historical_data
from src.pipeline.load import save_data_postgres
from src.pipeline.transform import transform_data, transform_historical_data

stop_event = threading.Event()


def handle_sigterm(_signum, _frame):
    """Gerencia o sinal de término (SIGTERM) para encerrar o pipeline.

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
    """Verifica se o horário atual está dentro do intervalo permitido para execução.

    O intervalo permitido é de segunda a sexta-feira, das 08:00 às 19:00
    (horário de São Paulo).

    Returns
    -------
    bool
        True se o horário atual estiver dentro do intervalo permitido,
        False caso contrário.
    """
    now = datetime.datetime.now(ZoneInfo("America/Sao_Paulo"))
    # Verifica se é fim de semana (5 = sábado, 6 = domingo)
    if now.weekday() >= 5:
        return False
    start = now.replace(hour=8, minute=0, second=0, microsecond=0)
    end = now.replace(hour=19, minute=0, second=0, microsecond=0)
    return start <= now <= end


def time_until_next_start():
    """Calcula o tempo restante até o próximo início permitido do pipeline.

    Considera que o pipeline só pode ser executado de segunda a sexta-feira,
    das 08:00 às 19:00.

    Returns
    -------
    datetime.timedelta
        Tempo restante até o próximo início permitido.
    """
    now = datetime.datetime.now(ZoneInfo("America/Sao_Paulo"))
    next_start = now.replace(hour=8, minute=0, second=0, microsecond=0)

    # Se já passou das 8h hoje, vai para o próximo dia
    if now >= next_start:
        next_start = next_start + datetime.timedelta(days=1)

    # Pula sábados e domingos
    while next_start.weekday() >= 5:  # 5 = sábado, 6 = domingo
        next_start = next_start + datetime.timedelta(days=1)

    return next_start - now


def create_tables(engine, logger):
    """Cria as tabelas no banco de dados PostgreSQL usando SQLAlchemy.

    Parameters
    ----------
    engine : sqlalchemy.engine.Engine
        Objeto engine do SQLAlchemy configurado para PostgreSQL.
    logger : logging.Logger
        Logger para registrar logs do processo.
    """
    Base.metadata.create_all(engine)
    logger.info("Tabelas criadas/verificadas com sucesso.")


def is_db_empty(Session):
    """
    Verifica se o banco de dados está vazio.
    Esta função consulta a tabela DolarData para verificar se não há registros.


    Parameters
    ----------
    Session : sqlalchemy.orm.session.Session
        Classe de sessão do SQLAlchemy para interagir com o banco.

    Returns
    -------
    bool
        True se o banco de dados estiver vazio (sem registros na tabela DolarData),
        False caso contrário.
    """
    session = Session()
    try:
        count = session.query(DolarData).count()
        return count == 0
    finally:
        session.close()


def pipeline(Session, logger):
    """
    Executa o pipeline ETL de cotação do dólar (USD-BRL).
    O pipeline verifica se o banco de dados está vazio. Se estiver, realiza uma carga histórica
    inicial dos últimos 3 meses. Caso contrário, executa o pipeline normal de extração,
    transformação e carga.

    Parameters
    ----------
    Session : sqlalchemy.orm.session.Session
        Classe de sessão do SQLAlchemy para interagir com o banco.
    logger : logging.Logger
        Logger para registrar logs do processo de ETL.
    """
    if is_db_empty(Session):
        with logfire.span("Carga histórica inicial"):
            logger.info(
                "Banco de dados vazio. Extraindo histórico dos últimos 3 meses..."
            )
            with logfire.span("Extraindo dados históricos"):
                data_hist = extract_historical_data(logger, days=90)
            if not data_hist:
                logger.error(
                    "Falha ao extrair dados históricos. Encerrando o pipeline."
                )
                return
            with logfire.span("Transformando dados históricos"):
                transformed_list = transform_historical_data(data_hist)
            with logfire.span("Salvando dados históricos no PostgreSQL"):
                for item in transformed_list:
                    save_data_postgres(Session, item, logger)
            logger.info("Carga histórica concluída com sucesso.")
        return
    # Pipeline normal
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
    """Executa o pipeline em loop contínuo com controle de horário.

    O pipeline executa apenas dentro do horário permitido (08:00-19:00, dias úteis).
    Fora do horário, aguarda e faz logs informativos.

    Parameters
    ----------
    Session : sqlalchemy.orm.session.Session
        Classe de sessão do SQLAlchemy para interagir com o banco.
    logger : logging.Logger
        Logger para registrar logs do pipeline.
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
                f"Fora do horário permitido (08:00-19:00). "
                f"Tempo restante até o próximo início: {hours:02d}:{minutes:02d}:{seconds:02d}. "
                f"Checando novamente em 10 minutos..."
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
