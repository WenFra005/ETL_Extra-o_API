"""
Módulo responsável pelo endpoint de saúde (health check) do serviço.
"""

import os

from flask import Flask

app = Flask(__name__)


@app.route("/")
def health():
    """
    Endpoint de saúde do serviço. Retorna uma mensagem indicando que o serviço está ativo.
    """
    return "Serviço ativo e funcionando!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
