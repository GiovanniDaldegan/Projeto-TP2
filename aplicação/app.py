from flask import Flask
from flask_socketio import SocketIO

from routes import set_routes

socketio = SocketIO()

# controladores
from modules.db_controller import DBController

# listeners
from modules import product_list


def create_app():
    """! Cria a aplicação Flask
    
    @return  app  Instância da aplicação Flask.
    """
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "tp2"

    db_controller = DBController(app.root_path)

    db_controller.create_tables()

    socketio.init_app(app)

    return app


if __name__ == "__main__":
    app = create_app()

    set_routes(app)


    socketio.run(app=app, port=5000)

