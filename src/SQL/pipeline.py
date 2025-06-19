from logging import basicConfig, getLogger
import logging
import time
from venv import logger
from dotenv import load_dotenv
import logfire
import requests
from datetime import UTC, datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from database import Base, DolarData

logfire.configure()
basicConfig(handlers=[logfire.LogfireLoggingHandler()])
logger = getLogger(__name__)
logger.setLevel(logging.INFO)
logfire.instrument_requests()
logfire.instrument_sqlalchemy()

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def create_tables():
    Base.metadata.create_all(engine)
    logger.info("Tabelas criadas com sucesso.")

def extract_data():
    url = 'https://economia.awesomeapi.com.br/json/last/USD-BRL'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Erro ao acessar a API: {response.status_code} - {response.text}")
        return None
    
def transform_data(data):
    moeda_origem = data['USDBRL']['code']
    moeda_destino = data['USDBRL']['codein']
    valor_de_compra = data['USDBRL']['bid']
    timestamp_moeda = datetime.fromtimestamp(int(data['USDBRL']['timestamp']), UTC)
    timestamp_criacao = datetime.now()

    data_transformed = {
        "moeda_origem": moeda_origem,
        "moeda_destino": moeda_destino,
        "valor_de_compra": valor_de_compra,
        "timestamp_moeda": timestamp_moeda,
        "timestamp_criacao": timestamp_criacao
    }

    return data_transformed

def save_data_postgres(data):
    session = Session()
    try:
        novo_registro = DolarData(**data)
        session.add(novo_registro)
        session.commit()
        logger.info(f"[{data['timestamp_criacao'].strftime('%d/%m/%y %H:%M:%S')}] Dados salvos com sucesso no banco de dados PostgreSQL.")
    except Exception as e:
        logger.error(f"Erro ao salvar dados no PostgreSQL: {e}")
        session.rollback()
    finally:
        session.close()

def pipeline():
    with logfire.span("Executando o pipeline de dados"):

        with logfire.span("Extraindo dados"):
            data = extract_data()
        
        if not data:
            logger.error("Nenhum dado foi extraído. Encerrando o pipeline.")
            return
        
        with logfire.span("Transformando dados"):
            transformed_data = transform_data(data)
        
        with logfire.span("Salvando dados no PostgreSQL"):
            save_data_postgres(transformed_data)
        
        logger.info("Pipeline de dados concluído com sucesso.")

if __name__ == "__main__":
    create_tables()
    logger.info("Iniciando o pipeline de dados...")

    while True:
        try:
            pipeline()
            logger.info("Aguardando 1 minuto para a próxima execução...")
            time.sleep(60)
        except KeyboardInterrupt:
            logger.info("Pipeline interrompido pelo usuário.")
            break
        except Exception as e:
            logger.error(f"Ocorreu um erro inesperado: {e}")
            time.sleep(30)    