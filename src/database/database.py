"""
Módulo de definição do modelo de dados e ORM para a tabela dolar_data no banco PostgreSQL.
"""

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class DolarData(Base):
    """
    Classe que representa a tabela `dolar_data` no banco de dados.

    Parameters
    ----------
    Base : sqlalchemy.orm.declarative_base
        Classe base do SQLAlchemy para a definição de modelos ORM.
    """

    __tablename__ = "dolar_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    moeda_origem = Column(String(3), nullable=False)
    moeda_destino = Column(String(3), nullable=False)
    valor_de_compra = Column(Float, nullable=False)
    timestamp_moeda = Column(DateTime(timezone=True), nullable=False)
    timestamp_criacao = Column(DateTime(timezone=True), nullable=False)
