"""! @package i_account
    Interface de eventos SocketIO das telas de login e cadastro de conta.
"""

from __main__ import socketio, db_controller

@socketio.on("register")
def register_account(data):
    """! Solicita a criação de conta.
    
    Chama a função do controlador do BD que cria registro de conta e comunica ao
    cliente se a conta foi criada com sucesso.

    @sa db_controller.DBController.create_account()
    """

    if not db_controller.create_account(data["acc_type"], data["username", data["password"]]):
        socketio.emit("register-failed")
        return
    
    socketio.emit("register-success")


# TODO #1: recebe evento de login, valida a conta no BD e envia p cliente o
# objeto retornado pelo BD
# > usar db_controller.get_account()

#@socketio.on("login")
# def log_user(data)
#    socketio.emit("logged")
