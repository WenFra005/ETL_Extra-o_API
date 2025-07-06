import os
from dotenv import load_dotenv
import pandas as pd
import psycopg2
import streamlit as st


load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")


def read_data_from_db():
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            password=POSTGRES_PASSWORD,
            user=POSTGRES_USER,
            port=POSTGRES_PORT,
            database=POSTGRES_DB,
        )
        query = """
        SELECT
            moeda_origem,
            moeda_destino,
            valor_de_compra,
			timestamp_moeda AT TIME ZONE 'America/Sao_Paulo' AS timestamp_moeda
		FROM dolar_data 
        ORDER BY timestamp_moeda DESC
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return pd.DataFrame()
