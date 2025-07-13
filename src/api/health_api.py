"""
Módulo responsável pelo endpoint de saúde (health check) do serviço.
Este módulo define um endpoint `/health` que retorna o status do serviço em formato JSON.
"""

import os

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/health")
def health():
    """
    Endpoint de saúde do serviço.
    Este endpoint retorna um JSON simples indicando que o serviço está ativo e funcionando.

    Returns
    -------
    dict
        Status do serviço em formato JSON.
    """
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
