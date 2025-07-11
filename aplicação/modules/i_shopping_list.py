"""! @package i_shopping_list
    Interface de eventos da tela de lista de compras
"""

from __main__ import socketio, db_controller


@socketio.on("shopping-lists")
def send_shopping_lists(user_id):
    lists = db_controller.get_shopping_lists(user_id)

    socketio.emit("shopping-lists", lists)


@socketio.on("get-shopping-list")
def send_product_list(list_id):
    shopping_list = db_controller.get_product_list(list_id)

    socketio.emit("shopping-list", shopping_list)
