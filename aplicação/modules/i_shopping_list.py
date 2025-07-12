"""! @package i_shopping_list
    Interface de eventos da tela de lista de compras
"""

from __main__ import socketio, db_controller

def send_all_lists(id_user:int):
    lists = db_controller.get_shopping_lists(id_user)

    socketio.emit("all-shopping-lists", [])
    

@socketio.on("get-all-shopping-lists")
def send_shopping_lists(id_user):
    send_all_lists(id_user)

@socketio.on("create-shopping-list")
def create_list(list_data):
    """! Responde ao evento "create-list" e cria lista de compras

    @param  list_data  Dicionário com "name" - nome da lista, "id_user".

    @sa db_controller.DBController.create_shopping_list()
    """

    db_controller.create_shopping_list(list_data["name"], list_data["id_user"])
    send_all_lists(list_data["id_user"])

@socketio.on("delete-list")
def delete_list(id_list):
    """! Responde ao evento "delete-list" e deleta lista de compras.

    @param  id_list  ID da lista a ser deletada.

    @sa db_controller.DBController.delete_product_list()
    """

    db_controller.delete_product_list(id_list)

@socketio.on("get-shopping-list")
def send_product_list(id_list):
    """! Responde ao evento "get-shopping-list" e envia detalhes de lista de compras.

    @param  id_list  ID da lista requerida.

    @sa db_controller.DBController.get_product_list()
    """

    shopping_list = db_controller.get_product_list(id_list)

    socketio.emit("shopping-list", shopping_list)

@socketio.on("add-to-list")
def add_to_list(data):
    """! Responde ao evento "add-to-list" e adiciona produto a lista ou atualiza
    sua quantidade na lista.

    @param  data  Dicionário com "id_list", "id_product", "quantity" -
    quantidade do produto (int).

    @sa db_controller.DBController.add_product_to_list()
    """

    db_controller.add_product_to_list(data["id_list"], data["id_product"], data["quantity"])

@socketio.on("remove-from-list")
def remove_from_list(data):
    """! Responde ao evento "remove-from-list" e remove item de lista.

    @param  data  Dicionário com "id_list", "id_product".

    @sa db_controller.DBController.remove_product_from_list()
    """
    
    db_controller.remove_product_from_list(data["id_list"], data["id_product"])

@socketio.on("set-product-taken")
def set_taken(data):
    """! Responde ao evento "set-product-taken" e atualiza produto em lista como pego ou
    não pego

    @param  data  Dicionário com "id_list", "id_product", "taken" - bool
    definindo se produto foi pego ou não.

    @sa db_controller.DBController.set_product_taken()
    """

    db_controller.set_product_taken(data["id_list"], data["id_product"], data["taken"])
