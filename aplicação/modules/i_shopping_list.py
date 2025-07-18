"""! @package i_shopping_list
    Interface de eventos da tela de lista de compras
"""

from __main__ import socketio, db_controller


def send_all_lists(id_user: int):
    lists = db_controller.get_all_shopping_lists(id_user)
    socketio.emit("all-shopping-lists", lists)

def send_list(id_list:int):
    shopping_list = db_controller.get_shopping_list(id_list)
    socketio.emit("shopping-list", shopping_list)
    
@socketio.on("get-all-shopping-lists")
def send_shopping_lists(id_user):
    send_all_lists(id_user)


@socketio.on("create-shopping-list")
def create_list(data):
    """! Responde ao evento "create-list" e cria lista de compras

    @param  data  Dicionário com "name" - nome da lista, "id_user".

    @sa db_controller.DBController.create_shopping_list()
    """

    db_controller.create_shopping_list(data["id_user"], data["name"])
    send_all_lists(data["id_user"])


@socketio.on("delete-list")
def delete_list(data):
    """! Responde ao evento "delete-list" e deleta lista de compras.

    @param  data  Dicionário com "id_user" e "id_list".

    @sa db_controller.DBController.delete_product_list()
    """

    db_controller.delete_shopping_list(data["id_list"])
    send_all_lists(data["id_user"])


@socketio.on("get-shopping-list")
def send_product_list(id_list):
    """! Responde ao evento "get-shopping-list" e envia detalhes de lista de compras.

    @param  id_list  ID da lista requerida.

    @sa db_controller.DBController.get_shopping_list()
    """

    shopping_list = db_controller.get_shopping_list(id_list)

    socketio.emit("shopping-list", shopping_list)

@socketio.on("get-best-market")
def get_best_market(list:list[dict]):
    n_items = len(list)
    complete = []
    relation = {}
    best = [0, 0]
    for item in list:
        sellers = db_controller.get_product_sellers(item['product_id'])
        for s in sellers:
            market = s['id_market']
            if(market in relation):
                relation[market]['available'] += 1
                relation[market]['total_price'] += (s['price']  * item['quantity'])
            else:
                relation[market] = {
                    "id_market" : market,
                    "market_name" : s["market_name"],
                    "available" : 1,
                    "total_price" : s['price']  * item['quantity']
                }
            if(relation[market]['available'] > best[0]):
                best[0] = relation[market]['available']
                best[1] = market
            elif((relation[market]['available'] == best[0]) and (relation[market]['total_price'] < relation[best[1]]['total_price'])):
                best[0] = relation[market]['available']
                best[1] = market
            if(relation[market]['available'] == n_items):
                complete.append(relation[market])
    if(complete):
        #sort complete array by total_price
        out = {
            "complete" : True,
            "options" : complete
        }
        return out
    else:
        out = {
            "complete" : False,
            "options" : relation[best[1]]
        }
        return out

@socketio.on("add-to-list")
def add_to_list(data):
    """! Responde ao evento "add-to-list" e adiciona produto a lista ou atualiza
    sua quantidade na lista.

    @param  data  Dicionário com "id_list", "id_product", "quantity" -
    quantidade do produto (int).

    @sa db_controller.DBController.add_product_to_list()
    """

    db_controller.add_product_to_list(data["id_list"], data["id_product"], data["quantity"])
    send_list(data["id_list"])


@socketio.on("remove-from-list")
def remove_from_list(data):
    """! Responde ao evento "remove-from-list" e remove item de lista.

    @param  data  Dicionário com "id_list", "id_product".

    @sa db_controller.DBController.remove_product_from_list()
    """

    db_controller.remove_product_from_list(data["id_list"], data["id_product"])
    send_list(data["id_list"])


@socketio.on("set-product-taken")
def set_taken(data):
    """! Responde ao evento "set-product-taken" e atualiza produto em lista como pego ou
    não pego

    @param  data  Dicionário com "id_list", "id_product", "taken" - bool
    definindo se produto foi pego ou não.

    @sa db_controller.DBController.set_product_taken()
    """

    db_controller.set_product_taken(data["id_list"], data["id_product"], data["taken"])
    send_list(data["id_list"])

