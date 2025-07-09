"""! @package i_account
    Interface de eventos SocketIO das telas de login e cadastro de conta.
"""

from __main__ import socketio, db_controller

@socketio.on("register")
def register_account(data):
    """! Solicita a criação de conta.
    
    Chama a função do controlador do BD que cria registro de conta e comunica ao
    cliente se a conta foi criada com sucesso.
    """

    if not db_controller.create_account(data):
        socketio.emit("register-failed")
        return
    
    socketio.emit("register-success")

#@socketio.on("login")