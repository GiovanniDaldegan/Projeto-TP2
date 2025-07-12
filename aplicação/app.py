"""! Script principal da aplicação"""

import os

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
    def index():
        return render_template("index.html")

    return app



if __name__ == "__main__":
    ## @var app
    # Aplicação Flask.
    app = create_app()

    socketio.run(app, "0.0.0.0", 5000, allow_unsafe_werkzeug=True)
