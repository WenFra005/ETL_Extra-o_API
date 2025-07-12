"""
Módulo responsável pelo dashboard Streamlit para visualização dos dados do dólar.
"""

import datetime
import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine

from src.database.database import DolarData

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
        query = """
        SELECT
            moeda_origem,
            moeda_destino,
            valor_de_compra,
			timestamp_moeda AT TIME ZONE 'America/Sao_Paulo' AS timestamp_moeda
		FROM dolar_data 
        ORDER BY timestamp_moeda DESC
        """
        df = pd.read_sql(query, engine)
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

        # Converter timestamp para datetime
        df["timestamp_moeda"] = pd.to_datetime(df["timestamp_moeda"])
        df = df.sort_values(by="timestamp_moeda")

        # Botões de zoom para o gráfico
        st.subheader("Evolução do preço do Dólar")

        # Criar botões de período
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            if st.button("Última Hora", key="hora"):
                st.session_state.periodo = "hora"
        with col2:
            if st.button("Último Dia", key="dia"):
                st.session_state.periodo = "dia"
        with col3:
            if st.button("Última Semana", key="semana"):
                st.session_state.periodo = "semana"
        with col4:
            if st.button("Último Mês", key="mes"):
                st.session_state.periodo = "mes"
        with col5:
            if st.button("Todos", key="todos"):
                st.session_state.periodo = "todos"

        # Inicializar período se não existir
        if "periodo" not in st.session_state:
            st.session_state.periodo = "todos"

        # Filtrar dados baseado no período selecionado
        agora = datetime.datetime.now()

        if st.session_state.periodo == "hora":
            df_filtrado = df[
                df["timestamp_moeda"] >= agora - datetime.timedelta(hours=1)
            ]
            periodo_texto = "Última Hora"
        elif st.session_state.periodo == "dia":
            df_filtrado = df[
                df["timestamp_moeda"] >= agora - datetime.timedelta(days=1)
            ]
            periodo_texto = "Último Dia"
        elif st.session_state.periodo == "semana":
            df_filtrado = df[
                df["timestamp_moeda"] >= agora - datetime.timedelta(weeks=1)
            ]
            periodo_texto = "Última Semana"
        elif st.session_state.periodo == "mes":
            df_filtrado = df[
                df["timestamp_moeda"] >= agora - datetime.timedelta(days=30)
            ]
            periodo_texto = "Último Mês"
        else:  # todos
            df_filtrado = df
            periodo_texto = "Todos os Dados"

        # Mostrar período selecionado
        st.write(f"**Período selecionado:** {periodo_texto}")

        # Exibir gráfico com dados filtrados
        if not df_filtrado.empty:
            st.line_chart(
                data=df_filtrado,
                x="timestamp_moeda",
                y="valor_de_compra",
                use_container_width=True,
            )
        else:
            st.warning(f"Nenhum dado disponível para o período: {periodo_texto}")

        st.subheader("Dados Estatísticos")
        col1, col2, col3 = st.columns(3)

        # Verificar se há dados filtrados antes de calcular métricas
        if not df_filtrado.empty:
            # Acessar valores diretamente do DataFrame
            preco_atual = df_filtrado["valor_de_compra"].iloc[-1]
            preco_maximo = df_filtrado["valor_de_compra"].max()
            preco_minimo = df_filtrado["valor_de_compra"].min()

            col1.metric("Preço Atual", f"R$ {preco_atual:.2f}")
            col2.metric("Preço Máximo", f"R$ {preco_maximo:.2f}")
            col3.metric("Preço Mínimo", f"R$ {preco_minimo:.2f}")
        else:
            col1.metric("Preço Atual", "N/A")
            col2.metric("Preço Máximo", "N/A")
            col3.metric("Preço Mínimo", "N/A")
    else:
        st.warning("Nenhum dado disponível para exibição.")


if __name__ == "__main__":
    main()
