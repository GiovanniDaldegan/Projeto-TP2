"""! Script principal da aplicação"""

import os

from flask import request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import Flask, render_template
from flask_socketio import SocketIO


## @var socketio
#    Objeto do servidor Flask-SocketIO
socketio = SocketIO()


# módulos básicos
from modules.db_controller import DBController

## @var db_controller
# Objeto controlador do banco de dados da aplicação
db_controller = DBController(os.path.dirname(os.path.realpath(__file__)))


# listeners
from modules import i_product_search, i_shopping_list, i_account, i_product


def create_app():
    """! Cria a aplicação Flask

    @return  Instância da aplicação Flask.
    """

    # inicialização dos módulos básicos

    db_controller.connect()
    db_controller.initialize()


    # inicialização da aplicação

    app = Flask(__name__)
    app.config["SECRET_KEY"] = "tp2"

    socketio.init_app(app)

    # índice da aplicação
    @app.route("/")
    
    @app.route("/produto/novo", methods=["POST"])
    def cadastrar_produto():
        nome = request.form["nome"]
        # Se o formulário tiver campos para mercado e preço, inclua-os:
        # id_market = int(request.form["id_market"])
        # preco = float(request.form["preco"])
        imagem = request.files["imagem"]

        if imagem:
            nome_arquivo = secure_filename(imagem.filename)
            caminho_pasta = os.path.join("aplicação", "static", "img", "produtos")
            os.makedirs(caminho_pasta, exist_ok=True)
            caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)
            imagem.save(caminho_arquivo)
            caminho_relativo = f"img/produtos/{nome_arquivo}"
        else:
            caminho_relativo = None

        # Ajuste a chamada conforme o método implementado no seu DBController
        db_controller.create_product(nome, caminho_relativo)
        # Se houver campos de mercado/preço:
        # db_controller.create_product(nome, id_market, preco, caminho_relativo)

        return redirect(url_for("index"))

    def index():
        return render_template("index.html")

    return app



if __name__ == "__main__":
    ## @var app
    # Aplicação Flask.
    app = create_app()

    socketio.run(app, "0.0.0.0", 5000, allow_unsafe_werkzeug=True)
