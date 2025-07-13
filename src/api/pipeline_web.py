"""
Este módulo define um serviço web Flask que executa um pipeline ETL em background.
Ele configura o ambiente de logging, a conexão com o banco de dados PostgreSQL e inicia o pipeline
em uma thread separada. O serviço expõe um endpoint `/health-pipeline` para verificar a saúde do serviço.
"""

import os
import threading

from flask import Flask, jsonify

from src.main import configure_ambient_logging, configure_database, loop_pipeline

app = Flask(__name__)

# Inicializa o pipeline em background assim que o módulo é importado (necessário para Gunicorn)
logger = configure_ambient_logging()
engine, Session = configure_database()
pipeline_thread = threading.Thread(target=loop_pipeline, args=(Session, logger))
pipeline_thread.start()


@app.route("/health-pipeline")
def health_pipeline():
    """
    Endpoint de saúde do serviço de pipeline.
    Este endpoint retorna um JSON simples indicando que o serviço está ativo e funcionando.
    Returns
    -------
    dict
        Status do serviço em formato JSON.
    """
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    # Este bloco permite rodar o pipeline ETL no Render, expondo um endpoint Flask para health
    # check.
    # O pipeline é executado em background (thread) e o Flask mantém o serviço ativo.
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
