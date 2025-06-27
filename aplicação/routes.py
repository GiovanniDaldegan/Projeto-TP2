"""! @package routes
  Define as rotas e as páginas da aplicação.
"""

from flask import render_template

def set_routes(app):
    """! Define todas as rotas da aplicação e suas templates HTML.
    
    @param  app  Aplicação Flask.

    Assertivas de entrada
      - app representa aplicação ativa    
    """

    # índice da aplicação
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/pesquisar")
    def product_feed():
        return render_template("product_feed.html")
