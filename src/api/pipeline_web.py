"""
Módulo para rodar o pipeline ETL como Web Service no Render.
Expõe um endpoint HTTP para health check e executa o pipeline em background.
"""

import os
import threading

from flask import Flask

from main import configure_ambient_logging, configure_database, loop_pipeline

app = Flask(__name__)

# Inicializa o pipeline em background assim que o módulo é importado (necessário para Gunicorn)
logger = configure_ambient_logging()
engine, Session = configure_database()
pipeline_thread = threading.Thread(target=loop_pipeline, args=(Session, logger))
pipeline_thread.start()


@app.route("/")
def health():
    return "Pipeline rodando!"


if __name__ == "__main__":
    # Este bloco permite rodar o pipeline ETL no Render, expondo um endpoint Flask para health
    # check.
    # O pipeline é executado em background (thread) e o Flask mantém o serviço ativo.
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
