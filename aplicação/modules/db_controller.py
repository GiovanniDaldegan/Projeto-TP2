#import sqlite3

class DBController:
    """! Controlador do banco de dados.

        Fornece a interface com o banco de dados.\n
        Cria e administra as tabelas da aplicação.
    """

    def __init__(self):
        """! Construtor da classe"""
        self.tables_ok = False
    
    def create_tables(self):
        """! Cria todas as tabelas da aplicação.

        Cria as tabelas:
        - PRODUCTS (id_prod:PK, name, price, rating)
        - MARKETS (id_mark:PK, name, location, rating)
        - CATEGORIES (id_cat:PK, category)
        - market_products (id_mark:PK:FK, id_prod:PK:FK)
        - product_categories (id_prod:PK:FK, id_cat:PK:FK)
        """

        print("Criando tabelas...")
        self.tables_ok = True
