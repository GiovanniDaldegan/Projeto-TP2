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