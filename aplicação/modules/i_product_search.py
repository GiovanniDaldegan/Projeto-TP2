"""! @package i_product_search
    Interface de eventos SocketIO da tela de pesquisa de produtos.
"""

from __main__ import socketio, db_controller

@socketio.on("get-product-list")
def send_product_list(data):
    """! Envia a lista de produtos que atendem à pesquisa do cliente.

    Ao receber o nome pesquisado e filtros selecionados na pesquisa do cliente,
    chama a função que busca os produtos que os atendem no BD e envia a lista
    de produtos para o cliente (sendo que cada item dela é um dicionário com as
    informações de um produto.

    @sa db_controller.DBController.search_products()
    """

    product_list = db_controller.search_products(search_term=data["search_term"], filters=data["filters"])

    socketio.emit("product-list", product_list)

@socketio.on("get-categories")
def send_categories():
    """! Envia a lista de todas as categorias de produtos disponíveis.

    @sa db_controller.DBController.get_categories()
    """
    socketio.emit("categories", db_controller.get_categories())