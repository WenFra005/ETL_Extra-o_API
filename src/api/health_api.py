""" Este módulo contém o endpoint de saúde do serviço."""
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
