import time
from dotenv import load_dotenv
import requests
from datetime import UTC, datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from database import Base, DolarData

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
    print("Tabelas criadas com sucesso.")

def extract_data():
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
    response = requests.get(url)
    data = response.json()
    
    return data

def transform_data(data):
    moeda_origem = data['USDBRL']['code']
    moeda_destino = data['USDBRL']['codein']
    valor_de_compra = data['USDBRL']['bid']
    timestamp_moeda = datetime.fromtimestamp(int(data['USDBRL']['timestamp']), UTC)
    timestamp_criacao = datetime.now(UTC)

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
    novo_registro = DolarData(**data)
    session.add(novo_registro)
    session.commit()
    session.close()
    print("Dados salvos com sucesso no banco de dados PostgreSQL.")

if __name__ == "__main__":
    create_tables()
    print("Iniciando o pipeline de dados...")

    while True:
        try:
            data = extract_data()
            transformed_data = transform_data(data)
            print("Dados transformados:", transformed_data)
            save_data_postgres(transformed_data)
            print("Aguardando 1 minuto para a próxima execução...")
            time.sleep(60)
        except KeyboardInterrupt:
            print("Pipeline interrompido pelo usuário.")
            break
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            print("Tentando novamente após 30 segundos...")
            time.sleep(30)
    print("Pipeline finalizado.")
    