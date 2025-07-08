import sys
from venv import logger

from flask import Flask

app = Flask(__name__)


@app.route("/")
def health():
    """
    Endpoint de saúde do serviço. Retorna uma mensagem indicando que o serviço está ativo.

    Returns
    -------
    str
        Uma mensagem indicando que o serviço está ativo.
    """
    return "Serviço ativo e funcionando!"


def handle_sigterm(_signum, _frame):
    logger.info("Recebido sinal de término (SIGTERM). Encerrando o pipeline...")
    sys.exit(0)
