"""! @package db_controller
    Módulo gerenciador do BD,

    Cria e monitora tabelas do banco de dados, além de consultá-las em busca de
    itens requisitados pelo cliente.
"""

import os
import sqlite3


class DBController:
    """! Controlador do banco de dados.

    Fornece a interface com o banco de dados.\n
    Cria e administra as tabelas da aplicação utilizando a biblioteca SQLite3
    para Python.
    """

    ## @var cursor_ok
    # Flag que indica se o cursor foi inicializado ou não.

    ## @var path_databases:str
    # String que guarda o caminho do diretório dos bancos de dados.

    ## @var cursor
    # Cursor (SQLite3) do BD.

    def __init__(self, app_root_dir):
        """! Construtor de DBController
        
        Inicialza o atributo cursor_ok como falso e guarda o caminho do
        diretório dos banco de dados no atributo path_databases.
        """

        self.cursor_ok = False
        self.path_databases = os.path.join(app_root_dir, "databases")
        self.populated = False  # variável exclusiva para testes e demonstração


    def set_cursor(self):
        """! Define o cursor do BD.
        
        Checa se existem o diretório "databases" e o arquivo "tables.db" dentro
        dele e os cria se não existirem. Após isso, conecta o BD e guarda seu
        cursor no atributo cursor da classe.
        """
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
            name         TEXT     NOT NULL,

            UNIQUE (name)
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

        # TODO: gerar id único para cada linha de tabela (tabela 
        #       específica com autoincrement?)


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
            print("[BD] ERRO: falta(m) tabela(s).")
            return False
        return True


    def populate(self):
        """! Popula as tabelas para fins de teste e demonstração."""
        if not self.is_db_ok() or self.populated:
            return

        self.cursor.execute(
            """
            INSERT INTO PRODUCT (id_product, name, price, rating)
            VALUES
                (00, "Veja Multiuso", 799, 45),
                (01, "Serenata do Amor", 327, 50),
                (02, "DVD Pirata vindo do Caribe", 1799, 25)
            """)
        
        self.cursor.execute(
            """
            INSERT INTO MARKET (id_market, name, latitude, longitude, rating)
            VALUES
                (03, "G Barbosa", 3887191112792959, -7705624540977456, 00)
            """)

        self.cursor.execute(
            """
            INSERT INTO CATEGORY (id_category, name)
            VALUES
                (04, "Limpeza"),
                (05, "Mídia"),
                (06, "Zero Lactose"),
                (07, "Gostoso")
            """)

        self.cursor.execute(
            """
            INSERT INTO _MARKET_PRODUCT (id_market, id_product)
            VALUES
                (03, 00),
                (03, 01),
                (03, 02)
            """)

        self.cursor.execute(
            """
            INSERT INTO _PRODUCT_CATEGORY (id_product, id_category)
            VALUES
                (00, 04),
                (00, 06),
                (00, 07),
                (01, 07),
                (02, 05),
                (02, 07)
            """)

        self.populated = True

