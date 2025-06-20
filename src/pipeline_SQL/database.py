from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime, UTC

Base = declarative_base()


class DolarData(Base):
    __tablename__ = "dolar_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    moeda_origem = Column(String(3), nullable=False)
    moeda_destino = Column(String(3), nullable=False)
    valor_de_compra = Column(Float, nullable=False)
    timestamp_moeda = Column(
        DateTime, default=lambda: datetime.now(UTC), nullable=False
    )
    timestamp_criacao = Column(
        DateTime, default=lambda: datetime.now(UTC), nullable=False
    )
