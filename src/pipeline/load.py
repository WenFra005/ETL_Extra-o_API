"""
Módulo responsável pelo carregamento dos dados transformados no banco de dados PostgreSQL.
"""


def save_data_postgres(Session, data, logger):
    """
    Salva os dados transformados no banco de dados PostgreSQL. Utiliza uma sessão do SQLAlchemy para
    adicionar um novo registro na tabela DolarData. Se ocorrer um erro, a transação é revertida.

    Parameters
    ----------
    Session : sqlalchemy.orm.session.Session
        Uma classe de sessão do SQLAlchemy para interagir com o banco de dados.

    data : dict
        Um dicionário contendo os dados transformados, que deve conter as chaves:
        - moeda_origem
        - moeda_destino
        - valor_de_compra
        - timestamp_moeda
        - timestamp_criacao
    logger : logging.Logger
        Um objeto logger configurado para registrar logs do pipeline de dados.
    """
    from src.database.database import DolarData

    session = Session()
    try:
        novo_registro = DolarData(**data)
        session.add(novo_registro)
        session.commit()
        logger.info(
            f"[{data['timestamp_criacao'].strftime('%d/%m/%y %H:%M:%S')}] "
            f"Dados salvos com sucesso no banco de dados PostgreSQL."
        )
    except Exception as e:
        logger.error(f"Erro ao salvar dados no PostgreSQL: {e}")
        session.rollback()
    finally:
        session.close()
