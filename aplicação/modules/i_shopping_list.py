"""! @package i_shopping_list
    Interface de eventos da tela de lista de compras
"""

from __main__ import socketio, db_controller


@socketio.on("shopping-lists")
def send_shopping_lists():
    # lists = db_controller.get_shopping_lists()

    socketio.emit("shopping-lists", )


@socketio.on("get-shopping-list")
def send_product_list(list_id):
    # shopping_list = db_controller.get_product_list(list_id)

    socketio.emit("shopping-list", )
