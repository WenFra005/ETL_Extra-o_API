"""
Módulo para definição do modelo de dados da tabela `dolar_data` no banco de dados.
"""

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy import DateTime

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
