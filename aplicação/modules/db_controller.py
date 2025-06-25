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
        
        self.tables_dict = {
            "PRODUCT" : {
                "columns" : [
                    "id_product INTEGER PRIMARY KEY",
                    "name TEXT NOT NULL",
                    "price INTEGER",
                    "rating INTEGER"
                ],
                "entries" : [
                    (0, "Veja Multiuso", 799, 45),
                    (1, "Serenata do Amor", 327, 50),
                    (2, "DVD Pirata vindo do Caribe", 1799, 25)
                ]
            },
            "MARKET" : {
                "columns" : [
                    "id_market INTEGER PRIMARY KEY",
                    "name TEXT NOT NULL",
                    "latitude INTEGER",
                    "longitude INTEGER",
                    "rating INTEGER"
                ],
                "entries" : [
                    (3, "G Barbosa", 3887191112792959, -7705624540977456, 00)
                ]
            },
            "CATEGORY" : {
                "columns" : [
                    "id_category INTEGER PRIMARY KEY",
                    "name TEXT NOT NULL"
                ],
                "entries" : [
                    (4, "Limpeza"),
                    (5, "Mídia"),
                    (6, "Zero Lactose"),
                    (7, "Gostoso")
                ]
            },
            "_MARKET_PRODUCT" : {
                "columns" : [
                    "id_market INTEGER",
                    "id_product INTEGER"
                ],
                "entries" : [
                    (3, 0),
                    (3, 1),
                    (3, 2)
                ]
            },
            "_PRODUCT_CATEGORY" : {
                "columns" : [
                    "id_product INTEGER",
                    "id_category INTEGER"
                ],
                "entries" : [
                    (0, 4),
                    (0, 6),
                    (0, 7),
                    (1, 7),
                    (2, 5),
                    (2, 7)
                ]
            },
        }


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

        for table_name, table in self.tables_dict.items():
            column_names = [i.split()[0] for i in table["columns"]]

            self.cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {table_name} ({str(column_names)[1:-1]})"
            )
        
        # tabelas de relacionamentos

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

        present_tables = 0

        for table_name in self.tables_dict.keys():
            result = self.cursor.execute(
                f"""
                SELECT name
                FROM sqlite_master
                WHERE type='table'
                AND name='{table_name}';
                """).fetchall()

            if len(result) != 0:
                present_tables += 1

        if len(self.tables_dict.keys()) != present_tables:
            print("[BD] ERRO: falta(m) tabela(s).")
            return False
        return True


    def populate(self):
        """! Popula as tabelas para fins de teste e demonstração."""
        if not self.is_db_ok() or self.populated:
            return


        for tab_name, table in self.tables_dict.items():
            for entry in table["entries"]:
                column_names = [i.split()[0] for i in table["columns"]]

                self.cursor.execute(
                    f"""
                    INSERT INTO {tab_name} ({str(column_names)[1:-1].replace('\'', '')})
                    VALUES ({str(entry)[1:-1]})
                    """)

        self.populated = True

