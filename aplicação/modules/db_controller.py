"""! @package db_controller
    Módulo gerenciador do BD,

    Cria e monitora tabelas do banco de dados, além de consultá-las em busca de
    itens requisitados pelo cliente.
"""

import os
import sqlite3
from modules.utils import *


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

        Guarda o caminho do diretório dos banco de dados no atributo @ref
        path_databases e inicializa as variáveis membros da classe.

        @param  app_root_dir  Caminho do diretório do script que instancia o
        controlador
        """

        self.path_databases = os.path.join(app_root_dir, "databases")
        self.connection = None
        self.populated = False  # variável exclusiva para testes e demonstração

        self.tables_dict = {
            "PRODUCT": [
                "id_product",
                "name",
                "price",
                "rating"
            ],
            "MARKET": [
                "id_market",
                "name",
                "latitude",
                "longitude",
                "rating"
            ],
            "CATEGORY": [
                "id_category",
                "name"
            ],
            "_MARKET_PRODUCT": [
                "id_market",
                "id_product"
            ],
            "_PRODUCT_CATEGORY": [
                "id_product",
                "id_category"
            ]
        }

    def connect(self):
        """! Define o cursor e a conexão do BD.

        Verifica se há conexão, caso não, inicializa o diretorio caso ele não exista,
        bem como a conexão e o @ref cursor.
        """
        try:
            if self.connection is None:
                if not os.path.isdir(self.path_databases):
                    os.mkdir(self.path_databases)
                self.connection = sqlite3.connect(os.path.join(
                    self.path_databases, "tables.db"), check_same_thread=False)

        except sqlite3.Error as e:
            print_error("[Erro BD]", "falha na conexão com o BD", e)
        except os.error as e:
            print_error("[Erro os]", "falha ao criar caminho do BD", e)

    def close(self):
        """! Fecha a conexão, evitando vazamentos e acesso indevido"""
        try:
            if self.connection:
                self.connection.close()
                self.connection = None
        except sqlite3.Error as e:
            print_error("[Erro BD]", "falha ao fechar a conexão com o BD", e)

    def get_cursor(self):
        """! Cria e retorna um cursor da conexão com o BD, desde que ela exista."""

        if self.connection:
            return self.connection.cursor()

    def initialize(self):
        """! Inicializa o Banco de dados garantindo que as tabelas existam"""

        try:
            # Verifica se as tabelas principais existem
            required_tables = ['PRODUCT', 'MARKET', 'CATEGORY']
            cursor = self.get_cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = [table[0] for table in cursor.fetchall()]

            # print(f"Tabelas existentes: {existing_tables}")  # Debug

            # Se faltar alguma tabela obrigatória
            if not all(table in existing_tables for table in required_tables):
                # print("Criando tabelas...")  # Debug
                self.create_tables()
                #print("Populando dados...")  # Debug
                self.populate()
            #else:
                #print("Tabelas já existem")  # Debug

        except sqlite3.Error as e:
            print_error("[Erro BD]", "falha na inicialização do BD", e)

    def create_tables(self):
        """! Cria todas as tabelas da aplicação.

        Cria as tabelas (nomes precedidos por _ são relacionamentos):
        - PRODUCT (id_product:PK, name, rating)
        - MARKET (id_market:PK, name, latitude, longitude, rating)
        - CATEGORY (name: PK)
        - _MARKET_PRODUCT (id_market:PK:FK, id_product:PK:FK, price)
        - _PRODUCT_CATEGORY (id_product:PK:FK, id_category:PK:FK)
        """

        create_script = """
            DROP TABLE IF EXISTS _PRODUCT_CATEGORY;
            DROP TABLE IF EXISTS _MARKET_PRODUCT;
            DROP TABLE IF EXISTS PRODUCT;
            DROP TABLE IF EXISTS MARKET;
            DROP TABLE IF EXISTS CATEGORY;
            DROP TABLE IF EXISTS ACCOUNT;
            DROP TABLE IF EXISTS SHOPPING_LIST;
            DROP TABLE IF EXISTS _LIST_ITEM;


            CREATE TABLE "CATEGORY" (
                "name"   TEXT   NOT NULL  UNIQUE,
                PRIMARY KEY("name")
            );

            CREATE TABLE "MARKET" (
                "id_market"  INTEGER,
                "name"       TEXT      NOT NULL,
                "latitude"   REAL,
                "longitude"  REAL,
                "rating"     REAL,
                PRIMARY KEY("id_market" AUTOINCREMENT)
            );

            CREATE TABLE "PRODUCT" (
                "id_product"  INTEGER,
                "name"        TEXT     NOT NULL,
                "rating"      REAL,

                PRIMARY KEY("id_product" AUTOINCREMENT)
            );

            CREATE TABLE "_MARKET_PRODUCT" (
                "id_market"   INTEGER  NOT NULL,
                "id_product"  INTEGER  NOT NULL,
                "price"       REAL     NOT NULL,

                PRIMARY KEY("id_market","id_product"),
                FOREIGN KEY("id_market") REFERENCES "MARKET"("id_market"),
                FOREIGN KEY("id_product") REFERENCES "PRODUCT"("id_product")
            );

            CREATE TABLE "_PRODUCT_CATEGORY" (
                "id_product"     INTEGER  NOT NULL,
                "category_name"  TEXT     NOT NULL,

                PRIMARY KEY("id_product","category_name"),
                FOREIGN KEY("category_name") REFERENCES "CATEGORY"("name"),
                FOREIGN KEY("id_product") REFERENCES "PRODUCT"("id_product")
            );

            CREATE TABLE ACCOUNT (
                id_user   INTEGER  PRIMARY KEY,
                username  TEXT     NOT NULL  UNIQUE,
                password  TEXT     NOT NULL
            );

            CREATE TABLE SHOPPING_LIST (
                id_list  INTEGER  PRIMARY KEY,
                id_user  INTEGER  NOT NULL,
                name     TEXT     NOT NULL,

                FOREIGN KEY (id_user) REFERENCES ACCOUNT (id_user)
            );

            CREATE TABLE _LIST_ITEM (
                id_list     INTEGER,
                id_product  INTEGER,
                id_market   INTEGER,
                quantity      INTEGER  NOT NULL,
                taken       BOOLEAN  NOT NULL,

                PRIMARY KEY (id_list, id_product, id_market)
            );
        """

        index_script = """
            CREATE INDEX IF NOT EXISTS idx_productcategory_product ON _PRODUCT_CATEGORY(id_product);
            CREATE INDEX IF NOT EXISTS idx_productcategory_category ON _PRODUCT_CATEGORY(category_name);
        """

        view_script = """
            DROP VIEW IF EXISTS v_products_general;
            DROP VIEW IF EXISTS v_shopping_list;


            CREATE VIEW v_products_general AS
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
            GROUP BY p.id_product;


            CREATE VIEW v_shopping_list AS
            SELECT
                sl.id_list              AS  id_list,
                COUNT(li.id_product)    AS  n_items,
                SUM(mp.price * quantity)  AS  total_price,
                SUM(CASE
                        WHEN li.taken THEN mp.price * quantity
                        ELSE 0
                    END)                AS  cart_price
            FROM SHOPPING_LIST sl
            JOIN _LIST_ITEM li
                ON sl.id_list = li.id_list
            JOIN _MARKET_PRODUCT mp
                ON li.id_product = mp.id_product
                AND li.id_market = mp.id_market
            GROUP BY sl.id_list;
        """

        try:
            cursor = self.get_cursor()
            cursor.executescript(create_script)
            cursor.executescript(index_script)
            cursor.executescript(view_script)

            self.connection.commit()

            # TODO: adicionar atributo de imagens ao produto

        except sqlite3.Error as e:
            print_error("[Erro BD]", "falha ao estruturar o BD", e)
        except Exception as e:
            print(f"qual foi\n{e}")

    def is_db_ok(self):
        """! Checa se o banco de dados está correto.

        Primeiro, checa se há conexão. Se não há, conecta ao banco de dados.
        Então, checa se todas as tabelas estão presentes no banco de dados.

        @return Bool indicanto se o BD está correto ou não.
        """

        if self.connection is None:
            self.connect()

        present_tables = 0

        try:
            cursor = self.get_cursor()
            for table_name in self.tables_dict.keys():
                result = cursor.execute(
                    f"""
                    SELECT name
                    FROM sqlite_master
                    WHERE type='table'
                        AND name='{table_name}';
                    """).fetchall()

                if len(result) != 0:
                    present_tables += 1

            if len(self.tables_dict.keys()) != present_tables:
                print_error("[BD Inconsistente]", "falta(m) tabela(s)")
                return False
            return True

        except sqlite3.Error as e:
            print_error("[Erro BD]", "falha na checagem do BD", e)

    def populate(self):
        """! Popula as tabelas para fins de teste e demonstração."""

        if self.populated:
            return

        inserts = [
            """
            INSERT INTO "CATEGORY" ("name") VALUES
                ('Bebidas'),
                ('Laticínios'),
                ('Padaria'),
                ('Carnes'),
                ('Frios'),
                ('Hortifruti'),
                ('Mercearia'),
                ('Bebidas Alcoólicas'),
                ('Pet Shop'),
                ('Utilidades Domésticas'),
                ('Congelados'),
                ('Orgânicos'),
                ('Sem Glúten'),
                ('Importados');
            """,
            """
            INSERT INTO "MARKET" ("name", "latitude", "longitude", "rating") VALUES
                ('Supermercado Preço Bom', -23.5505, -46.6333, 4.2),
                ('Mercado Qualitativo', -23.5432, -46.6444, 4.5),
                ('Atacadão Economia', -23.5488, -46.6222, 3.9),
                ('Supermercado São Luiz', -23.5555, -46.6111, 4.1),
                ('Mercado Natural', -23.5522, -46.6555, 4.7);
            """,

            """
            INSERT INTO "PRODUCT" ("name", "rating") VALUES
                ('Veja Multiuso 500ml', 4.5),
                ('Sabão em Pó Omo 1kg', 4.3),
                ('Arroz Tio João 5kg', 4.7),
                ('Feijão Carioca 1kg', 4.6),
                ('Leite Integral Parmalat 1L', 4.4),
                ('Café Pilão 500g', 4.8),
                ('Açúcar União 1kg', 4.2),
                ('Óleo de Soja Liza 900ml', 4.0),
                ('Macarrão Spaghetti Renata 500g', 4.5),
                ('Cerveja Heineken 350ml', 4.9),
                ('Refrigerante Coca-Cola 2L', 4.7),
                ('Sabonete Dove 90g', 4.6),
                ('Shampoo Pantene 400ml', 4.5),
                ('Desinfetante Pinho Sol 1L', 4.3),
                ('Papel Higiênico Neve 30m', 4.8),
                ('Salmão Fresco Filé 500g', 4.7),
                ('Queijo Mussarela Fresco 1kg', 4.6),
                ('Pão de Forma Integral 500g', 4.3),
                ('Ração para Cães Adultos 15kg', 4.5),
                ('Vinho Tinto Chileno 750ml', 4.8);
            """,
            """
            INSERT INTO "_PRODUCT_CATEGORY" ("id_product", "category_name") VALUES
                (2, 'Limpeza'), (12, 'Limpeza'), (13, 'Limpeza'), (14, 'Limpeza'), (15, 'Limpeza'),
                (3, 'Mercearia'), (4, 'Mercearia'), (6, 'Mercearia'), (7, 'Mercearia'), (8, 'Mercearia'), (9, 'Mercearia'),
                (10, 'Bebidas Alcoólicas'), (11, 'Bebidas'), (20, 'Bebidas Alcoólicas'),
                (5, 'Laticínios'), (17, 'Laticínios'),
                (16, 'Carnes'), (17, 'Frios'),
                (18, 'Padaria'), (18, 'Orgânicos'),
                (19, 'Pet Shop'),
                (1, 'Utilidades Domésticas'),
                (5, 'Orgânicos'),
                (10, 'Importados'),
                (11, 'Importados'),
                (14, 'Utilidades Domésticas'),
                (15, 'Utilidades Domésticas'),
                (16, 'Congelados'),
                (20, 'Importados');
            """,
            """
            INSERT INTO "_MARKET_PRODUCT" ("id_market", "id_product", "price") VALUES
                (1, 2, 11.90), (1, 3, 21.90), (1, 4, 8.99), (1, 5, 3.99),
                (1, 6, 6.49), (1, 7, 3.49), (1, 8, 4.99), (1, 9, 3.29), (1, 10, 5.99),
                (1, 11, 7.49), (1, 12, 2.19), (1, 13, 16.90), (1, 14, 6.99), (1, 15, 10.99),

                (2, 1, 8.49), (2, 3, 22.50), (2, 5, 4.29), (2, 6, 6.99), (2, 7, 3.79),
                (2, 10, 6.49), (2, 11, 7.99), (2, 12, 2.49), (2, 13, 17.90), (2, 16, 31.90),
                (2, 17, 19.90), (2, 18, 6.49), (2, 19, 89.90), (2, 20, 39.90),

                (3, 2, 10.90), (3, 3, 20.90), (3, 4, 7.99), (3, 8, 4.79), (3, 9, 2.99),
                (3, 10, 5.79), (3, 11, 7.29), (3, 14, 6.49), (3, 15, 9.99), (3, 16, 29.90),
                (3, 17, 17.90), (3, 19, 85.00), (3, 20, 37.90),

                (4, 1, 9.90), (4, 2, 13.50), (4, 5, 4.99), (4, 6, 7.49), (4, 7, 4.29),
                (4, 10, 7.90), (4, 12, 2.99), (4, 13, 19.90), (4, 16, 35.90), (4, 17, 22.90),
                (4, 18, 7.90), (4, 20, 44.90),

                (5, 3, 24.90), (5, 4, 10.90), (5, 5, 5.49), (5, 6, 8.90), (5, 8, 5.90),
                (5, 9, 4.49), (5, 11, 8.90), (5, 16, 37.90), (5, 17, 24.90), (5, 18, 8.90),
                (5, 19, 99.90), (5, 20, 49.90);
            """,
            """
            INSERT INTO ACCOUNT (username, password) VALUES
                ("123", "123")
            """,
            """
            INSERT INTO SHOPPING_LIST (id_user, name) VALUES
                (1, "aaa"),
                (1, "bbb")
            """,
            """
            INSERT INTO _LIST_ITEM (id_list, id_product, id_market, quantity, taken) VALUES
                (1, 5, 1, 1, FALSE),
                (1, 2, 1, 3, FALSE),
                (1, 3, 1, 2, FALSE),
                (1, 6, 1, 1, TRUE),
                (2, 3, 1, 1, TRUE),
                (2, 4, 1, 1, TRUE),
                (2, 5, 1, 1, FALSE),
                (2, 6, 1, 1, FALSE)
            """
        ]

        try:
            cursor = self.get_cursor()
            for q in inserts:
                cursor.execute(q)

            # sobe os inserts para o arquivo .db, se quiser manter apenas em memoria reova
            self.connection.commit()
            self.populated = True

            print(cursor.execute("SELECT * FROM v_shopping_list").fetchall())

        except sqlite3.Error as e:
            print_error("[Erro BD]", "falha ao tentar popular o BD", e)

    def get_categories(self):
        """! Consulta quais são as categorias registradas.

        @return Lista com todas as categorias em formato string.
        """

        try:
            cursor = self.get_cursor()
            return [i[0] for i in cursor.execute("SELECT * FROM CATEGORY").fetchall()]

        except sqlite3.Error as e:
            print_error("[Erro BD]", "falha ao consultar categorias", e)

    def search_products(self, search_term=None, filters=None, limit=20):
        """!
        @brief brief Busca produtos com filtros avançados

        @param search_term: String de busca (Opcional) - busca por correspondência no nome do produto

        @param filters: Dicionario de filtros (Opcional) - com os seguintes parâmetros:
            - min_price: float - preço mínimo
            - max_price: float - preço máximo
            - min_rating: float - avaliação mínima (0-5)
            - category: string - nome exato da categoria
            - sort: string - nome exato do atributo de ordenação

        @param limit: int - limite de resultados (padrão: 20)

        @return Lista de dicionários contendo:
            - id: int - ID do produto
            - name: str - Nome do produto
            - rating: float - Avaliação
            - categories: list[str] - Lista de categorias
            - price_range: tuple(min, max) - Faixa de preços
            - avg_price: float - Preço médio

        @note
        **Atributos de Ordenação Validos**
        - min_price
        - max_price
        - rating
        - categories
        - name
        """

        query = "SELECT * FROM v_products_general"
        params = []  # valores que entram nos placeholders(?)
        conditions = []  # Clausulas where

        # Filtro termos de busca
        if search_term:
            conditions.append("name LIKE ? COLLATE NOCASE")
            params.append(f"%{search_term}%")
        # Outros Filtros
        if filters:
            if ("min_price" in filters):
                conditions.append("min_price >= ?")
                params.append(filters['min_price'])
            if ("max_price" in filters):
                conditions.append("min_price <= ?")
                params.append(filters['max_price'])
            if ("category" in filters):
                conditions.append("categories LIKE ?")
                params.append(f"{filters['category']}%")
            if ("min_rating" in filters):
                conditions.append("rating >= ?")
                params.append(filters['min_rating'])

        # Montagem da query
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        if filters and "sort" in filters:
            query += f" ORDER BY {filters['sort']}"
        else:
            query += " ORDER BY name"

        query += f" LIMIT {abs(int(limit))}"

        self.connect()
        try:
            cursor = self.get_cursor()
            cursor.execute(query, params)
            return self.format_results(cursor.fetchall())

        except sqlite3.Error as e:
            print_error("[Erro BD]", "falha na pesquisa de produtos", e)

    def format_results(self, rows):
        """! Organiza os dados brutos em uma estrutura mais útil

        @param  rows  Lista de linhas resultantes de consulta.
        """

        formatted = []
        for row in rows:
            formatted.append({
                "id": row[0],
                "name": row[1],
                "rating": row[2],
                "categories": row[3].split(',') if row[3] else [],
                "price_range": (row[4], row[5]),
                "avg_price": row[6]
            })
        return formatted

    def get_all_shopping_lists(self, user_id):
        """! Busca todas as listas de um usuário, dado seu ID.

        @param  user_id  ID do usuário.

        @return Lista de nomes das listas de compras do usuário.
        """

        if not self.is_db_ok():
            return

        try:
            cursor = self.get_cursor()
            cursor.execute(
                f"SELECT name FROM SHOPPING_LIST WHERE id_user = {user_id}")
            return cursor.fetchall()

        except sqlite3.Error as e:
            print_error(
                "[Erro BD]", "falha na busca de listas de compras de usuário", e)

    def get_shopping_list(self, list_id):
        """! Busca os dados de dada lista de compras.

        @param  list_id  ID da lista.
        """

        if not self.is_db_ok():
            return

        try:
            cursor = self.get_cursor()
            cursor.execute(
                f"SELECT * FROM v_shopping_list WHERE id_list = {list_id}")
            return cursor.fetchall()

        except sqlite3.Error as e:
            print_error("[Erro BD]", "falha na busca de lista de compras", e)

    def create_shopping_list(self, name:str, user_id:int):
        """! Registra uma nova lista de compras de um usuário."""

        try:
            cursor = self.get_cursor()
            cursor.execute(f"""INSERT INTO SHOPPING_LIST (id_user, name) VALUES ({user_id}, {name})""")

        except sqlite3.Error as e:
            print_error("[Erro BD]", "falha na inserção de lista de compras", e)
    
    def add_product_to_list(self, id_list:int, id_market:int, id_product:int, quantity:int):
        """! Adiciona dado produto a dada lista.
        
        @param  id_list     ID da lista.
        @param  id_market   ID do mercado do produto.
        @param  id_product  ID do produto.
        @param  quantity    Quantidade escolhida do produto.
        """

        try:
            cursor = self.get_cursor()
            cursor.execute(f"INSERT INTO _LIST_ITEM VALUES ({id_list}, {id_market}, {id_product}, {quantity}, {quantity}, FALSE)")

        except sqlite3.Error as e:
            print_error("[Erro BD]", "falha na inserção de produto na lista de compras", e)

    def set_product_taken(self, id_list:int, id_market:int, id_product:int, taken:bool):
        """! Define o status do produto de lista como \"pego\".
        
        @param id_list     ID da lista.
        @param id_market   ID do mercado do produto.
        @param id_product  ID do produto.
        """

        try:
            cursor = self.get_cursor()
            cursor.execute(
                f"""
                UPDATE TABLE _LIST_ITEM
                SET taken={taken}
                WHERE id_list={id_list}
                    AND id_market={id_market}
                    AND id_product={id_product}
                """)

        except sqlite3.Error as e:
            print_error("[Erro BD]", "falha na atualização de produto na lista de compras", e)
