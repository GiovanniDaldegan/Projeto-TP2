import os
import sqlite3


class DBController:
    """! Controlador do banco de dados.

        Fornece a interface com o banco de dados.\n
        Cria e administra as tabelas da aplicação.
    """

    def __init__(self, app_root_dir):
        """! Construtor de DBController"""
        self.cursor_ok = False
        self.path_databases = os.path.join(app_root_dir, "databases")


    def set_cursor(self):
        if not os.path.isdir(self.path_databases):
            os.mkdir(self.path_databases)

        db_connection = sqlite3.connect(os.path.join(self.path_databases, "tables.db"))
        self.cursor = db_connection.cursor()
        self.cursor_ok = True


    def create_tables(self):
        """! Cria todas as tabelas da aplicação.

        Cria as tabelas (nomes precedidos por _ são relacionamentos):
        - PRODUCT (id_product:PK, name, price, rating)
        - MARKET (id_market:PK, name, location, rating)
        - CATEGORY (id_category:PK, category)
        - _MARKET_PRODUCT (id_market:PK:FK, id_product:PK:FK)
        - _PRODUCT_CATEGORY (id_product:PK:FK, id_category:PK:FK)
        """

        if not self.cursor_ok:
            self.set_cursor()
        
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS PRODUCT(
            id_product  INTEGER   PRIMARY KEY,
            name     TEXT     NOT NULL,
            price    INTEGER,
            rating   INTEGER
            );
            """)

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS MARKET(
            id_market  INTEGER  PRIMARY KEY,
            name       TEXT     NOT NULL,
            latitude   INTEGER,
            longitude  INTEGER,
            rating     INTEGER
            );
            """)

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS CATEGORY(
            id_category  INTEGER  PRIMARY KEY,
            category     TEXT     NOT NULL,

            UNIQUE (category)
            );
            """)

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS _MARKET_PRODUCT(
            id_market   INTEGER,
            id_product  INTEGER,
            
            PRIMARY KEY (id_market, id_product),
            FOREIGN KEY (id_market)  REFERENCES  MARKET(id_market)
            );
            """)

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS _PRODUCT_CATEGORY(
            id_product   INTEGER,
            id_category  TEXT,
            
            PRIMARY KEY (id_product, id_category),
            FOREIGN KEY (id_product)   REFERENCES  PRODUCT(id_product),
            FOREIGN KEY (id_category)  REFERENCES  CATEGORY(id_category)
            );
            """)


    def is_db_ok(self):
        """! Checa se o banco de dados está correto.
        
        Checa se todas as tabelas estão presentes no banco de dados.
        """
        if not self.cursor_ok:
            self.set_cursor()
        
        # TODO: centralizar o registro de quais tabelas devem existir pra evitar
        #       inconsistências

        table_names = ["PRODUCT", "MARKET", "CATEGORY", "_MARKET_PRODUCT", "_PRODUCT_CATEGORY"]
        present_tables = 0

        for table_name in table_names:
            result = self.cursor.execute(
                f"""
                SELECT name
                FROM sqlite_master
                WHERE type='table'
                AND name='{table_name}';
                """).fetchall()
            
            if len(result) != 0:
                present_tables += 1


        if len(table_names) != present_tables:
            return False
        
        return True
