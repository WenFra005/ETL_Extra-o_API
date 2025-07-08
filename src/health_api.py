from flask import Flask
from waitress import serve

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


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=10000)
