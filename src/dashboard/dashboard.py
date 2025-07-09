"""
Módulo responsável pelo dashboard Streamlit para visualização dos dados do dólar.
"""

import os

import pandas as pd
import psycopg2
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")


def read_data_from_db():
    """
    Extrai dados do banco de dados PostgreSQL e retorna um DataFrame com os dados do dólar.

    Returns
    -------
    df : pd.DataFrame
        Um DataFrame contendo os dados do dólar.

    Raises
    ------
    Exception
        Se ocorrer um erro ao conectar ao banco de dados.
    """
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


def main():
    """
    Função principal do dashboard Streamlit para visualização dos dados do dólar.

    Returns
    -------
    None

    Raises
    ------
    Exception
        Se ocorrer um erro ao conectar ao banco de dados ou ao ler os dados.
    """
    st.set_page_config(
        page_title="Dashboard de Dados do Dólar", page_icon=":dollar:", layout="wide"
    )
    st.title("Dashboard de Preços do Dólar")
    st.write(
        f"Este dashboard exibe os preços do dólar coletados periodicamente em um banco PostgreSQL."
    )

    df = read_data_from_db()

    if not df.empty:
        st.subheader("Dados do Dólar recentes")
        st.dataframe(df)

        df["timestamp_moeda"] = pd.to_datetime(df["timestamp_moeda"])
        df = df.sort_values(by="timestamp_moeda")

        st.subheader("Evolução do preço do Dólar")
        st.line_chart(
            data=df,
            x="timestamp_moeda",
            y="valor_de_compra",
            use_container_width=True,
        )

        st.subheader("Dados Estatísticos")
        col1, col2, col3 = st.columns(3)
        col1.metric("Preço Atual", f"R$ {df['valor_de_compra'].iloc[-1]:.2f}")
        col2.metric("Preço Máximo", f"R$ {df['valor_de_compra'].max():.2f}")
        col3.metric("Preço Mínimo", f"R$ {df['valor_de_compra'].min():.2f}")
    else:
        st.warning("Nenhum dado disponível para exibição.")


if __name__ == "__main__":
    main()
