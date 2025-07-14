"""! Teste das repostas de requisições do servidor

    Testa:
    - get-categories: requisição da lista de categorias de produtos existentes
    - get-product-list: requisição de lista de produtos com parâmetros de
      pesquisa (nome, categoria, faixa de preço)
"""

# iniciar servidor
# estabelecer cliente socketio
# fazer requisições

import socketio

sio = socketio.SimpleClient()
assert sio.sid == None
sio.connect('http://localhost:5000', transports=['websocket'])
assert sio.sid != None
assert sio.transport() == 'websocket'


def test_category_list_request():
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
            "sort": "min_price"
        }
    }
    sio.emit("get-product-list", search_query)
    event = sio.receive()
    assert event[0] == "product-list"
    assert event[1] != None
    assert len(event) == 2

# TODO: testes de cadastro de usuário

def test_get_all_shopping_lists():
    sio.emit("get-all-shopping-lists", 1)
    response = sio.receive()
    assert response[0] == "all-shopping-lists"
    assert response[1] != None
    if len(response[1]) != 0:
        assert "id" in response[1][0].keys()
        assert "name" in response[1][0].keys()

def test_create_shopping_list():
    sio.emit("create-shopping-list", {"id_user": 1, "name": "lista teste"})
    sio.receive()

def test_delete_shopping_list():
    sio.emit("delete-list", {"id_user": 1, "id_list": 1})
    sio.receive()

def test_get_shopping_list():
    sio.emit("get-shopping-list", 1)
    response = sio.receive()

    assert response[0] == "shopping-list"
    if len(response[1]) != 0:
        assert "product_id" in response[1][0].keys()
        assert "product_name" in response[1][0].keys()
        assert "quantity" in response[1][0].keys()
        assert "taken" in response[1][0].keys()

def test_add_to_shopping_list():
    sio.emit("add-to-list", {"id_list": 1, "id_product" : 5, "quantity" : 2})
    response = sio.receive()

    assert response[0] == "shopping-list"
    if len(response[1]) != 0:
        assert "product_id" in response[1][0].keys()
        assert "product_name" in response[1][0].keys()
        assert "quantity" in response[1][0].keys()
        assert "taken" in response[1][0].keys()

def test_remove_from_shopping_list():
    sio.emit("remove-from-list", {"id_list": 1, "id_product" : 5})
    response = sio.receive()

    assert response[0] == "shopping-list"
    if len(response[1]) != 0:
        assert "product_id" in response[1][0].keys()
        assert "product_name" in response[1][0].keys()
        assert "quantity" in response[1][0].keys()
        assert "taken" in response[1][0].keys()

def test_set_product_taken():
    sio.emit("set-product-taken", {"id_list": 1, "id_product": 2, "taken": True})
    event = sio.receive()
