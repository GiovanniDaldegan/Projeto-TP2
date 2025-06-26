import os

from flask import Flask
from flask_socketio import SocketIO

from routes import set_routes

socketio = SocketIO()

# listeners
from modules import product_list

# módulos básicos
from modules.db_controller import DBController

db_controller = DBController(os.path.dirname(os.path.realpath(__file__)))

db_controller.create_tables()
db_controller.populate()



def create_app():
    """! Cria a aplicação Flask
    
    @return  app  Instância da aplicação Flask.
    """
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "tp2"

    socketio.init_app(app)

    return app


if __name__ == "__main__":
    app = create_app()

    set_routes(app)


    socketio.run(app=app, allow_unsafe_werkzeug=True, port=5000)

