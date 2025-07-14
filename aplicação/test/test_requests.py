import socketio

"""! Teste das repostas de requisições do servidor

    Testa:
    - get-categories: requisição da lista de categorias de produtos existentes
    - get-product-list: requisição de lista de produtos com parâmetros de
      pesquisa (nome, categoria, faixa de preço)
"""

# iniciar servidor
# estabelecer cliente socketio
# fazer requisições

sio = socketio.SimpleClient()
assert sio.sid == None
sio.connect("http://localhost:5000", transports=["websocket"])
assert sio.sid != None
assert sio.transport() == "websocket"


def test_category_request():
    sio.emit("get-categories")
    event = sio.receive()
    assert event[0] == "categories"
    assert event[1] != None
    assert len(event) == 2


def test_product_list_request():
    search_query = {
        "search_term": "Macarrão",
        "filters": {
            "min_price": 3.5,
            "max_price": 40.79,
            "min_rating": 2.2,
            "category": "Bebidas",
            "sort": "min_price",
        },
    }
    sio.emit("get-product-list", search_query)
    event = sio.receive()
    assert event[0] == "product-list"
    assert event[1] != None
    assert len(event) == 2
