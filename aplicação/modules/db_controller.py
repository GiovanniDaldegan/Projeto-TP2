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

    ## @var cursor
    # Cursor (SQLite3) do BD.

    ## @var connection
    # Conexão com o BD para enviar as mudanças para o arquivo de banco de dados.

    ## @var path_databases
    # String que guarda o caminho do diretório dos bancos de dados.

    ## @var tables_dict
    # Dicionário com os nomes das tabelas e o nome de suas colunas.
    #
    # Sua estrutura é a seguinte:
    # tables_dict = {
    #     "nome_tabela" : ["nome_coluna0", "nome_coluna1"],
    # }

    def __init__(self, app_root_dir):
        """! Construtor de DBController
        
        Inicialza o atributo cursor_ok como falso e guarda o caminho do
        diretório dos banco de dados no atributo path_databases.
        """

        self.cursor = None
        self.path_databases = os.path.join(app_root_dir, "databases")
        self.connection = None
        self.populated = False  # variável exclusiva para testes e demonstração

        self.tables_dict = {
            "PRODUCT" : [
                "id_product",
                "name",
                "price",
                "rating"
            ],
            "MARKET" : [
                "id_market",
                "name",
                "latitude",
                "longitude",
                "rating"
            ],
            "CATEGORY" : [
                "id_category",
                "name"
            ],
            "_MARKET_PRODUCT" : [
                "id_market",
                "id_product"
            ],
            "_PRODUCT_CATEGORY" : [
                "id_product",
                "id_category"
            ],
        }


    def connect(self):
        """! Define o cursor e a conexão do BD.

        Verifica se há conexão, caso não, inicializa o diretorio caso ele não exista,
        bem como a conexão e o cursor
        """
        if self.connection is None:
            if not os.path.isdir(self.path_databases):
                os.mkdir(self.path_databases)
            self.connection = sqlite3.connect(os.path.join(self.path_databases, "tables.db"))
            self.cursor = self.connection.cursor()

    def initialize(self):
        """! Inicializa o Banco de dados caso não exista"""
        self.connect()

        if not os.path.exists(self.db_path):  # Identifica primeira execução
            self.create_tables()
            self.populate()


    def create_tables(self):
        """! Cria todas as tabelas da aplicação.

        Cria as tabelas (nomes precedidos por _ são relacionamentos):
        - PRODUCT (id_product:PK, name, rating)
        - MARKET (id_market:PK, name, latitude, longitude, rating)
        - CATEGORY (name: PK)
        - _MARKET_PRODUCT (id_market:PK:FK, id_product:PK:FK, price)
        - _PRODUCT_CATEGORY (id_product:PK:FK, id_category:PK:FK)
        """

        if self.cursor is None:
            self.connect()

        # script cria todas as tabelas do banco
        self.cursor.executescript(
            """
            DROP TABLE IF EXISTS _PRODUCT_CATEGORY;
            DROP TABLE IF EXISTS _MARKET_PRODUCT;
            DROP TABLE IF EXISTS PRODUCT;
            DROP TABLE IF EXISTS MARKET;
            DROP TABLE IF EXISTS CATEGORY;

            CREATE TABLE "CATEGORY" (
                "name"	TEXT NOT NULL UNIQUE,
                PRIMARY KEY("name")
            );

            CREATE TABLE "MARKET" (
                "id_market"	INTEGER,
                "name"	TEXT NOT NULL,
                "latitude"	REAL,
                "longitude"	REAL,
                "rating"	REAL,
                PRIMARY KEY("id_market" AUTOINCREMENT)
            );

            CREATE TABLE "PRODUCT" (
                "id_product"	INTEGER,
                "name"	TEXT NOT NULL,
                "rating"	REAL,
                PRIMARY KEY("id_product" AUTOINCREMENT)
            );

            CREATE TABLE "_MARKET_PRODUCT" (
                "id_market"	INTEGER NOT NULL,
                "id_product"	INTEGER NOT NULL,
                "price"	REAL NOT NULL,
                PRIMARY KEY("id_market","id_product"),
                FOREIGN KEY("id_market") REFERENCES "MARKET"("id_market"),
                FOREIGN KEY("id_product") REFERENCES "PRODUCT"("id_product")
            );

            CREATE TABLE "_PRODUCT_CATEGORY" (
                "id_product"	INTEGER NOT NULL,
                "category_name"	TEXT NOT NULL,
                PRIMARY KEY("id_product","category_name"),
                FOREIGN KEY("category_name") REFERENCES "CATEGORY"("name"),
                FOREIGN KEY("id_product") REFERENCES "PRODUCT"("id_product")
            );
            """)

        """cria indices que auxiliam em joins e em querrys"""
        self.cusor.executescript(
            """
            CREATE INDEX IF NOT EXISTS idx_productcategory_product ON _PRODUCT_CATEGORY(id_product);
            CREATE INDEX IF NOT EXISTS idx_productcategory_category ON _PRODUCT_CATEGORY(category_name);
            """)

        """cria Views"""
        self.cusor.executescript(
            """
            CREATE VIEW IF NOT EXISTS v_product_details AS
            SELECT 
                p.id_product,
                p.name,
                p.rating,
                GROUP_CONCAT(DISTINCT pc.category_name) AS categories,
                MIN(mp.price) AS min_price,
                MAX(mp.price) AS max_price,
                AVG(mp.price) AS avg_price
            FROM PRODUCT p
            LEFT JOIN _PRODUCT_CATEGORY pc ON p.id_product = pc.id_product
            LEFT JOIN _MARKET_PRODUCT mp ON p.id_product = mp.id_product
            GROUP BY p.id_product  
            """)
        
        self.connection.commit() #sobe o banco para o arquivo .db, se quiser manter apenas em memoria reova


        # TODO: adicionar atributo de imagens ao produto


    def is_db_ok(self):
        """! Checa se o banco de dados está correto.
        
        Checa se todas as tabelas estão presentes no banco de dados.
        """

        if self.cursor is None:
            self.connect()

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

        inserts = [
        """INSERT INTO "CATEGORY" ("name") VALUES 
           ('Limpeza'), ('Mídia'), ('Zero Lactose'), ('Gostoso')""",
        
        """INSERT INTO "MARKET" ("name", "latitude", "longitude", "rating") VALUES
           ('G Barbosa', 38.87191112792959, -77.05624540977456, 0.0)""",
        
        """INSERT INTO "PRODUCT" ("name", "rating") VALUES
           ('Veja Multiuso', 45.0),
           ('Serenata do Amor', 50.0),
           ('DVD Pirata vindo do Caribe', 25.0)""",
        
        """INSERT INTO "_MARKET_PRODUCT" ("id_market", "id_product", "price") VALUES
           (1, 1, 7.99), (1, 2, 3.27), (1, 3, 17.99)""",
        
        """INSERT INTO "_PRODUCT_CATEGORY" ("id_product", "category_name") VALUES
           (1, 'Limpeza'), (1, 'Zero Lactose'),
           (2, 'Gostoso'), (3, 'Mídia') """
        ]

        for q in inserts:
            self.cursor.execute(q)

        self.connection.commit() #sobe os inserts para o arquivo .db, se quiser manter apenas em memoria reova
        self.populated = True


    def close(self):
        """Fecha a conexão, evitando vazamentos e acesso indevido"""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
