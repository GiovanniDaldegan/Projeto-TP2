"""! @package product_list
  Módulo para fornecer a lista de produtos cadastrados com base nos filtros
  aplicados e nome pesquisado.
  
  Baseado no nome e nos filtros, é chamada a função responsável por consultar o
  banco de dados e retornar uma lista com os produtos que atendem ao nome ou 
  filtros usados na busca.
"""

from __main__ import socketio

# ! EXEMPLO !
# listener do servidor: ativado quando recebe connect do cliente
@socketio.on("connect")
def send_product_list():
    print("DAMN")

    # servidor envia um evento "get-product-list" com um dicionário que vai ser serializado para JSON
    socketio.emit("get-product-list", {"product0" : {"name": "shampoo", "price": "R$$111111111.00000,00000"}})
