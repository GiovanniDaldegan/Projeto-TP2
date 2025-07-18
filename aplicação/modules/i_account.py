"""! @package i_account
    Interface de eventos SocketIO das telas de login e cadastro de conta.
"""

from __main__ import socketio, db_controller


@socketio.on("register-user")
def register_account(data):
    """! Solicita a criação de conta.

    Chama a função do controlador do BD que cria registro de conta e comunica ao
    cliente se a conta foi criada com sucesso.

    @sa db_controller.DBController.create_account()
    """

    if not db_controller.create_account(data["acc_type"], data["username"], data["password"]):
        socketio.emit("register-failed")
        return

    acc = db_controller.get_account(data["username"], data["password"])
    socketio.emit("logged", acc)


@socketio.on("login-user")
def log_user(data):
    acc = db_controller.get_account(data["username"], data["password"])

    if acc:
        socketio.emit("logged", acc)
