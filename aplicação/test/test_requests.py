"""! Teste das repostas de requisições do servidor

    Testa:
    - get-categories: requisição da lista de categorias de produtos existentes
    - get-produt-list: requisição de lista de produtos com parâmetros de
      pesquisa (nome, categoria, faixa de preço)
"""

# iniciar servidor
# estabelecer cliente socketio
# fazer requisições

"""
socketio.emit("get-categories")
search_query = {
    "search_term" : "Macarrão",
    "filters" : {
        "min_price" : 3.5,
        "max_price" : 40.79,
        "min_rating" : 2.2,
        "category" : "Bebidas",
        "sort" : "min_price"
    } 
}
socketio.emit("get-product-list", search_query)

# checar se os atributos dos produtos recebidos são pertinentes
"""
