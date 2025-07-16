"""! Script principal da aplicação"""

import sys
from pathlib import Path

from flask import Flask, render_template
from flask_socketio import SocketIO


## @var socketio
#    Objeto do servidor Flask-SocketIO
socketio = SocketIO()


# módulos básicos
from modules.db_controller import DBController

## @var db_controller
# Objeto controlador do banco de dados da aplicação

if sys.argv[0] == 'test':
    db_controller = DBController(str(Path(__file__).parent / "test"))
else:
    db_controller = DBController(str(Path(__file__).parent))


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
    def index():
        return render_template("index.html")

    # rota para a tela de login
    @app.route("/login")
    def login():
        return render_template("login.html")
    
    # rota para tela de cadastro
    @app.route("/cadastro")
    def create_product():
        return render_template("create_product.html") 
    
    # rota para URL dos produtos
    @app.route("/produto/<int:product_id>")
    def product_page(product_id):
        return render_template("index.html")
    
    # rota para tela de criar conta
    @app.route("/conta")
    def register():
        return render_template("create_account.html")
    return app


if __name__ == "__main__":
    ## @var app
    # Aplicação Flask.
    app = create_app()

    socketio.run(app, "0.0.0.0", 5000, allow_unsafe_werkzeug=True)
