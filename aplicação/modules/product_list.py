"""! @package product_list
  Módulo para fornecer a lista de produtos cadastrados com base nos filtros
  aplicados e nome pesquisado.
  
  Baseado no nome e nos filtros, é chamada a função responsável por consultar o
  banco de dados e retornar uma lista com os produtos que atendem ao nome ou 
  filtros usados na busca.
"""

from __main__ import socketio

@socketio.on("get-product-list")
def send_product_list(data):
    """! Envia a lista de produtos de acordo com o nome pesquisado e os filtros
    aplicados pelo usuário.
    
    Ao receber essas informações do usuário, chama a função que busca os
    produtos que os atendem no BD, formata os dados e envia a lista de produtos
    para o cliente.
    """
    
    print(f"nome: {data["product_name"]}\nfiltros: {data["filters"]}\n")
