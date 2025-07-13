"""! @package i_product
    Interface de eventos das telas de criação de produto e página de produto.
"""

from __main__ import socketio, db_controller


# TODO #6: tranquilin. listener que registra produto
# - dicionário data deve ter chaves "id_product", "id_market", "price"
# - chamar db_controller.create_product() para registrar

# @socketio.on("register-product")
# def register_product():


# TODO #7 tranquilin. listener que registra avaliação de produto
# - dicionário data: "id_product", "rating", "comment"

# @socketio.on("review-product")
# def review_produc(data):


# TODO #8: tranquilin. listener que envia detalhes de produto.
# - definir o que o data a seguir deve conter
# - buscar produto com db_controller.get_product()
# - enviar ao cliente o dicionário resultante

# @socketio.on("get-product")
# def send_product(data):

@socketio.on("add-review")
def add_reivew(data):
    """! Responde ao evento "add-review" e adiciona avaliação de produto

    @param  data  Dicionáio com "id_product", "rating" - nota dada ao produto,
    "comment" - comentário sobre o produto.

    @sa db_controller.DBController.add_product_review()
    """

    db_controller.add_product_review(data["id_product"], data["rating"], data["comment"])
