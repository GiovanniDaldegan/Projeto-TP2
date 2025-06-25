import os
import sqlite3


class DBController:
    """! Controlador do banco de dados.

        Fornece a interface com o banco de dados.\n
        Cria e administra as tabelas da aplicação.
    """

    def __init__(self, app_root_dir):
        """! Construtor de DBController"""
        self.tables_ok = False
        self.path_databases = os.path.join(app_root_dir, "databases")
    

    def create_tables(self):
        """! Cria todas as tabelas da aplicação.

        Cria as tabelas (nomes precedidos por _ são relacionamentos):
        - PRODUCT (id_product:PK, name, price, rating)
        - MARKET (id_market:PK, name, location, rating)
        - CATEGORY (id_category:PK, category)
        - _MARKET_PRODUCT (id_market:PK:FK, id_product:PK:FK)
        - _PRODUCT_CATEGORY (id_product:PK:FK, id_category:PK:FK)
        """

        if not os.path.isdir(self.path_databases):
            os.mkdir(self.path_databases)

        db_connection = sqlite3.connect(os.path.join(self.path_databases, "tables.db"))
        cursor = db_connection.cursor()
        
        cursor.execute("""CREATE TABLE PRODUCT(
                       id_product  INTEGER   PRIMARY KEY,
                       name     TEXT     NOT NULL,
                       price    INTEGER,
                       rating   INTEGER
                       );""")

        cursor.execute("""CREATE TABLE MARKET(
                       id_market  INTEGER  PRIMARY KEY,
                       name       TEXT     NOT NULL,
                       latitude   INTEGER,
                       longitude  INTEGER,
                       rating     INTEGER
                       );""")

        cursor.execute("""CREATE TABLE CATEGORY(
                       id_category  INTEGER  PRIMARY KEY,
                       category     TEXT     NOT NULL,
                       
                       UNIQUE (category)
                       );""")

        cursor.execute("""CREATE TABLE _MARKET_PRODUCT(
                       id_market   INTEGER,
                       id_product  INTEGER,
                       
                       PRIMARY KEY (id_market, id_product),
                       FOREIGN KEY (id_market)  REFERENCES  MARKET(id_market)
                       );""")

        cursor.execute("""CREATE TABLE _PRODUCT_CATEGORY(
                       id_product   INTEGER,
                       id_category  TEXT,
                       
                       PRIMARY KEY (id_product, id_category),
                       FOREIGN KEY (id_product)   REFERENCES  PRODUCT(id_product),
                       FOREIGN KEY (id_category)  REFERENCES  CATEGORY(id_category)
                       );""")
