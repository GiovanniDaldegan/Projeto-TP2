"""! @package i_product
    Interface de eventos das telas de criação de produto e página de produto.
"""

from __main__ import socketio, db_controller


@socketio.on("register-product")
def register_product(data):

    if "id_product" in data:
        db_controller.create_product(
            name=data["name"], id_market=int(data["id_market"]), price=int(data["price"]))
    else:
        db_controller.create_product(name=data["name"])

    # adicionar categorias do produto

@socketio.on("review-product")
def review_product(data):
    # sem checagem de erros! cuidado. Quando escrito, TODO#4 não tava pronto.
    db_controller.create_product(
        id_product=int(data["id_product"]), rating=int(data["rating"]), comment=data["comment"])


# TODO #8: tranquilin. listener que envia detalhes de produto.
# - definir o que o data a seguir deve conter
# - buscar produto com db_controller.get_product()
# - enviar ao cliente o dicionário resultante

@socketio.on("get-product")
def send_product(data):
    product = db_controller.get_product(id_product=int(data["id_product"]))
    socketio.emit("product", product)
