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

    ## @var tables_list
    # Lista com nomes de tabelas que devem existir no BD.

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

        self.tables_list = ["PRODUCT", "MARKET", "CATEGORY", "_MARKET_PRODUCT", "_PRODUCT_CATEGORY"]

    def connect(self):
        """! Define o cursor e a conexão do BD.

        Verifica se há conexão, caso não, inicializa o diretorio caso ele não exista,
        bem como a conexão e o @ref cursor.
        """

        if self.connection is None:
            if not os.path.isdir(self.path_databases):
                os.mkdir(self.path_databases)
            self.connection = sqlite3.connect(
                os.path.join(self.path_databases, "tables.db"), check_same_thread=False
            )

    def close(self):
        """! Fecha a conexão, evitando vazamentos e acesso indevido"""

        if self.connection:
            self.connection.close()
            self.connection = None

    def get_cursor(self):
        """! Cria e retorna um cursor da conexão com o BD, desde que ela exista."""

        if self.connection:
            return self.connection.cursor()

    def initialize(self):
        """! Inicializa o Banco de dados garantindo que as tabelas existam"""

        try:
            # Verifica se as tabelas principais existem
            required_tables = ["PRODUCT", "MARKET", "CATEGORY"]
            cursor = self.get_cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = [table[0] for table in cursor.fetchall()]

            # print(f"Tabelas existentes: {existing_tables}")  # Debug

            # Se faltar alguma tabela obrigatória
            if not all(table in existing_tables for table in required_tables):
                # print("Criando tabelas...")  # Debug
                self.setup_db()
                # print("Populando dados...")  # Debug
                self.populate()
            # else:
            # print("Tabelas já existem")  # Debug

        except sqlite3.Error as e:
            print_error("[Erro BD]", "falha na inicialização do BD", e)

    def setup_db(self):
        """! Cria todas as tabelas da aplicação.

        Cria as tabelas (nomes precedidos por _ são relacionamentos):
        - PRODUCT (id_product:PK, name)
        - MARKET (id_market:PK, name, latitude, longitude, rating)
        - CATEGORY (name: PK)
        - _MARKET_PRODUCT (id_market:PK:FK, id_product:PK:FK, price)
        - _PRODUCT_CATEGORY (id_product:PK:FK, id_category:PK:FK)
        """

        #DROP TABLE IF EXISTS _PRODUCT_CATEGORY;
        #DROP TABLE IF EXISTS _MARKET_PRODUCT;
        #DROP TABLE IF EXISTS PRODUCT;
        #DROP TABLE IF EXISTS MARKET;
        #DROP TABLE IF EXISTS CATEGORY;
        #DROP TABLE IF EXISTS ACCOUNT;
        #DROP TABLE IF EXISTS SHOPPING_LIST;
        #DROP TABLE IF EXISTS _LIST_ITEM;
        #DROP TABLE IF EXISTS PRODUCT_REVIEW;
        create_script = """
            CREATE TABLE IF NOT EXISTS "CATEGORY" (
                "name"   TEXT   NOT NULL  UNIQUE,
                PRIMARY KEY("name")
            );

            CREATE TABLE IF NOT EXISTS "MARKET" (
                "id_market"  INTEGER,
                "name"       TEXT      NOT NULL,
                "latitude"   INTEGER,
                "longitude"  INTEGER,
                "rating"     INTEGER,
                PRIMARY KEY("id_market" AUTOINCREMENT)
            );

            CREATE TABLE IF NOT EXISTS "PRODUCT" (
                "id_product"  INTEGER,
                "name"        TEXT     NOT NULL,

                PRIMARY KEY("id_product" AUTOINCREMENT)
            );

            CREATE TABLE IF NOT EXISTS "_MARKET_PRODUCT" (
                "id_market"   INTEGER  NOT NULL,
                "id_product"  INTEGER  NOT NULL,
                "price"       INTEGER  NOT NULL,

                PRIMARY KEY("id_market","id_product"),
                FOREIGN KEY("id_market") REFERENCES "MARKET"("id_market"),
                FOREIGN KEY("id_product") REFERENCES "PRODUCT"("id_product")
            );

            CREATE TABLE IF NOT EXISTS "_PRODUCT_CATEGORY" (
                "id_product"     INTEGER  NOT NULL,
                "category_name"  TEXT     NOT NULL,

                PRIMARY KEY("id_product","category_name"),
                FOREIGN KEY("category_name") REFERENCES "CATEGORY"("name"),
                FOREIGN KEY("id_product") REFERENCES "PRODUCT"("id_product")
            );

            CREATE TABLE IF NOT EXISTS ACCOUNT (
                id_user   INTEGER  PRIMARY KEY,
                acc_type  TEXT     NOT NULL,
                username  TEXT     NOT NULL  UNIQUE,
                password  TEXT     NOT NULL
            );

            CREATE TABLE IF NOT EXISTS SHOPPING_LIST (
                id_list  INTEGER  PRIMARY KEY AUTOINCREMENT,
                id_user  INTEGER  NOT NULL,
                name     TEXT     NOT NULL,

                FOREIGN KEY (id_user) REFERENCES ACCOUNT (id_user)
            );

            CREATE TABLE IF NOT EXISTS _LIST_ITEM (
                id_list     INTEGER,
                id_product  INTEGER,
                quantity    INTEGER  NOT NULL,
                taken       BOOLEAN  NOT NULL,

                PRIMARY KEY (id_list, id_product)
            );

            CREATE TABLE IF NOT EXISTS PRODUCT_REVIEW (
                id_review   INTEGER,
                id_product  INTEGER,
                rating      REAL,
                comment     TEXT,

                PRIMARY KEY ("id_review" AUTOINCREMENT),
                FOREIGN KEY("id_product") REFERENCES "PRODUCT"("id_product")
            );
        """

        index_script = """
            CREATE INDEX IF NOT EXISTS idx_productcategory_product ON _PRODUCT_CATEGORY(id_product);
            CREATE INDEX IF NOT EXISTS idx_productcategory_category ON _PRODUCT_CATEGORY(category_name);
        """

        view_script = """
            DROP VIEW IF EXISTS v_products_general;
            DROP VIEW IF EXISTS v_shopping_list;
            DROP VIEW IF EXISTS v_product_sellers;


            CREATE VIEW v_products_general AS
            SELECT
                p.id_product,
                p.name,
                AVG(pr.rating) AS rating,
                GROUP_CONCAT(DISTINCT pc.category_name) AS categories,
                MIN(mp.price) AS min_price,
                MAX(mp.price) AS max_price,
                AVG(mp.price) AS avg_price
            FROM PRODUCT p
			LEFT JOIN PRODUCT_REVIEW pr ON P.id_product = pr.id_product
            LEFT JOIN _PRODUCT_CATEGORY pc ON p.id_product = pc.id_product
            LEFT JOIN _MARKET_PRODUCT mp ON p.id_product = mp.id_product
            GROUP BY p.id_product;


            CREATE VIEW v_shopping_list AS
            SELECT 
				li.id_list,
                p.id_product,
				p.name,
				li.quantity,
				li.taken
			FROM _LIST_ITEM li 
			LEFT JOIN PRODUCT P ON li.id_product = p.id_product;

            CREATE VIEW IF NOT EXISTS v_product_sellers AS
            SELECT 
				p.id_product,
                m.id_market,
                m.name AS market_name,
                mp.price,
                m.rating AS market_rating,
                m.latitude,
                m.longitude
            FROM PRODUCT p
            LEFT JOIN _MARKET_PRODUCT mp ON p.id_product = mp.id_product
            LEFT JOIN MARKET m ON mp.id_market = m.id_market
            GROUP BY p.id_product, m.id_market;
        """

        cursor = self.get_cursor()
        cursor.executescript(create_script)
        cursor.executescript(index_script)
        cursor.executescript(view_script)

        self.connection.commit()

    def is_db_ok(self):
        """! Checa se o banco de dados está correto.

        Primeiro, checa se há conexão. Se não há, conecta ao banco de dados.
        Então, checa se todas as tabelas estão presentes no banco de dados.

        @return Bool indicanto se o BD está correto ou não.
        """

        if self.connection is None:
            self.connect()
            self.setup_db()

        present_tables = []

        cursor = self.get_cursor()
        for table_name in self.tables_list:
            result = cursor.execute(
                f"""
                SELECT name
                FROM sqlite_master
                WHERE type='table'
                    AND name='{table_name}';
                """
            ).fetchone()

            if result:
                present_tables.append(result[0])

        if len(self.tables_list) != len(present_tables):
            print(self.tables_list, '\n', present_tables)
            print_error("[BD Inconsistente]", "falta(m) tabela(s)")
            #return False
        return True

    def populate(self):
        """! Popula as tabelas para fins de teste e demonstração."""

        if self.populated or not self.is_db_ok():
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
            INSERT INTO "PRODUCT" ("name") VALUES
                ('Veja Multiuso 500ml'),
                ('Sabão em Pó Omo 1kg'),
                ('Arroz Tio João 5kg'),
                ('Feijão Carioca 1kg'),
                ('Leite Integral Parmalat 1L'),
                ('Café Pilão 500g'),
                ('Açúcar União 1kg'),
                ('Óleo de Soja Liza 900ml'),
                ('Macarrão Spaghetti Renata 500g'),
                ('Cerveja Heineken 350ml'),
                ('Refrigerante Coca-Cola 2L'),
                ('Sabonete Dove 90g'),
                ('Shampoo Pantene 400ml'),
                ('Desinfetante Pinho Sol 1L'),
                ('Papel Higiênico Neve 30m'),
                ('Salmão Fresco Filé 500g'),
                ('Queijo Mussarela Fresco 1kg'),
                ('Pão de Forma Integral 500g'),
                ('Ração para Cães Adultos 15kg'),
                ('Vinho Tinto Chileno 750ml');
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
            INSERT INTO ACCOUNT (acc_type, username, password) VALUES
                ("adm", "123", "123")
            """,
            """
            INSERT INTO SHOPPING_LIST (id_user, name) VALUES
                (1, "aaa"),
                (1, "bbb")
            """,
            """
            INSERT INTO _LIST_ITEM (id_list, id_product, quantity, taken) VALUES
                (1, 5, 1, FALSE),
                (1, 2, 3, FALSE),
                (1, 3, 2, FALSE),
                (1, 6, 1, TRUE),
                (2, 3, 1, TRUE),
                (2, 4, 1, TRUE),
                (2, 5, 1, FALSE),
                (2, 6, 1, FALSE)
            """,
            """
            INSERT INTO PRODUCT_REVIEW (id_product, rating, comment) VALUES
                (1, 3, 'aaaa'),
                (1, 2, 'aaaa'),
                (1, 5, 'aaaa'),
                (1, 4, 'aaaa'),
                (1, 2.4, 'aaaa'),
                (1, 3.3, 'aaaa'),
                (2, 3, 'aaaa'),
                (2, 1.5, 'aaaa'),
                (3, 4.6, 'aaaa'),
                (3, 5, 'aaaa'),
                (3, 3, 'aaaa'),
                (6, 2, 'aaaa'),
                (6, 0, 'aaaa')
            """,
        ]

        cursor = self.get_cursor()
        for q in inserts:
            cursor.execute(q)

        # sobe os inserts para o arquivo .db, se quiser manter apenas em memoria remova
        self.connection.commit()
        self.populated = True

    def get_categories(self):
        """! Consulta quais são as categorias registradas.

        @return Lista com todas as categorias em formato string.
        """

        if not self.is_db_ok():
            return

        cursor = self.get_cursor()
        return [i[0] for i in cursor.execute("SELECT * FROM CATEGORY").fetchall()]

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

        if not self.is_db_ok():
            return

        query = "SELECT * FROM v_products_general"
        params = []  # valores que entram nos placeholders(?)
        conditions = []  # Clausulas where

        # Filtro termos de busca
        if search_term:
            conditions.append("name LIKE ? COLLATE NOCASE")
            params.append(f"%{search_term}%")
        # Outros Filtros
        if filters:
            if "min_price" in filters:
                conditions.append("min_price >= ?")
                params.append(filters["min_price"])
            if "max_price" in filters:
                conditions.append("min_price <= ?")
                params.append(filters["max_price"])
            if "category" in filters:
                conditions.append("categories LIKE ?")
                params.append(f"{filters['category']}%")
            if "min_rating" in filters:
                conditions.append("rating >= ?")
                params.append(filters["min_rating"])

        # Montagem da query
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        if filters and "sort" in filters:
            query += f" ORDER BY {filters['sort']}"
        else:
            query += " ORDER BY name"

        query += f" LIMIT {abs(int(limit))}"

        cursor = self.get_cursor()
        cursor.execute(query, params)
        return self.format_product_search(cursor.fetchall())

    def format_product_search(self, rows):
        """! Organiza os dados brutos em uma estrutura mais útil

        @param  rows  Lista de linhas resultantes de consulta.
        """

        formatted = []
        for row in rows:
            formatted.append(
                {
                    "id": row[0],
                    "name": row[1],
                    "rating": row[2],
                    "categories": row[3].split(",") if row[3] else [],
                    "price_range": (row[4], row[5]),
                    "avg_price": row[6],
                }
            )
        return formatted

    def create_account(self, acc_type, username, password, no_commit:bool=False):
        """! Cadastra uma conta no BD.

        @param  acc_type  Tipo de conta (adm, user).
        @param  username  Nome do usuário.
        @param  password  Senha do usuário.
        """

        if not self.is_db_ok():
            return

        if self.account_exists(username):
            return

        cursor = self.get_cursor()
        cursor.execute(f"""
            INSERT INTO ACCOUNT (acc_type, username, password)
            VALUES ('{acc_type}', '{username}', '{password}')""")

        if not no_commit:
            self.connection.commit()
        return True

    def account_exists(self, username):
        """! Checa se conta existe no BD.

        @param  username  Nome do usuário.
        @param  password  Senha do usuário.
        """

        if not self.is_db_ok():
            return

        cursor = self.get_cursor()
        record = cursor.execute(f"""
            SELECT * FROM ACCOUNT
            WHERE username='{username}'"""
        ).fetchone()

        return self.format_account(record)

    def delete_account(self, id_user:int, no_commit=False):
        """! Deleta registro de conta.

        @param  id_user  ID da conta a ser deletada.
        """

        if not self.is_db_ok():
            return

        cursor = self.get_cursor()
        lists = self.get_all_shopping_lists(id_user)

        if lists:
            for i in lists:
                self.delete_shopping_list(i["id"], no_commit)

        cursor.execute(f"DELETE FROM ACCOUNT WHERE id_user={id_user}")

        if not no_commit:
            self.connection.commit()

    def get_account(self, username, password):
        """! Consulta e retorna nome e tipo de usuário

        @param  username  Nome do usuário.
        @param  password  Senha do usuário.

        @return Dicionário com chaves "user_name" e "type"
        """

        if not self.is_db_ok():
            return

        cursor = self.get_cursor()
        record = cursor.execute(f"""
            SELECT id_user, acc_type, username FROM ACCOUNT
            WHERE username='{username}'
                AND password='{password}'
        """).fetchone()

        if not record:
            return

        return self.format_account(record)

    def format_account(self, acc):
        if acc:
            if len(acc) >= 3:
                return {
                        "id_user"  : acc[0],
                        "acc_type" : acc[1],
                        "username" : acc[2]
                }

    def get_all_shopping_lists(self, user_id:int) -> list[str]:
        """! Busca todas as listas de um usuário, dado seu ID.

        @param  user_id  ID do usuário.

        @return Lista de nomes das listas de compras do usuário.
        """

        if not self.is_db_ok():
            return

        cursor = self.get_cursor()
        cursor.execute(f"SELECT * FROM SHOPPING_LIST WHERE id_user={user_id}")

        lists = cursor.fetchall()

        if len(lists) == 0:
            return
        return self.format_shopping_lists(lists)

    def format_shopping_lists(self, lists: list) -> list[dict]:
        """! Formata uma lista de listas de compras em um dicionário com id e
        nome de cada lista

        @param  lists  Listas de compras.

        @return Lista com dicionários de lista de compras.
        """

        return [{"id": l[0], "name": l[2]} for l in lists]

    def get_shopping_list(self, id_list) -> list[dict]:
        """! Busca os dados de dada lista de compras.

        @param  id_list  ID da lista.

        @return Dicionário com  as informações da lista.
        """

        if not self.is_db_ok():
            return

        cursor = self.get_cursor()
        cursor.execute(f"SELECT * FROM v_shopping_list WHERE id_list={id_list}")

        return self.format_shopping_list(cursor.fetchall())

    def format_shopping_list(self, shopping_list:list) -> list[dict]:
        """! Formata e retorna uma lista de compras em uma lista de dicionários.

        @param shopping_lists  Lista com infomações da listas de compras.

        @return uma lista de dicionários com informações de lista de compras.
        """
        # o tamanho da lista é a quantidade de produtos diferentes nela
        formatted = []
        for item in shopping_list:
            formatted.append({"product_id": item[1], "product_name": item[2], "quantity": item[3], "taken": item[4]})
        # o tamanho da lista é a quantidade de produtos diferentes nela
        return formatted

    def create_shopping_list(self, user_id:int, name:str, no_commit:bool=False):
        """! Registra uma nova lista de compras de um usuário."""

        if not self.is_db_ok():
            return

        cursor = self.get_cursor()
        cursor.execute(f"""
            INSERT INTO SHOPPING_LIST (id_user, name)
            VALUES ({user_id}, "{name}")
            """)

        if not no_commit:
            self.connection.commit() #Sobe mudanças para o arquivo


    def delete_shopping_list(self, id_list:int, no_commit:bool=False):
        """! Deleta lista de compras.

        @param  id_list  ID da lista de compras a ser deletada
        """

        if not self.is_db_ok():
            return

        cursor = self.get_cursor()
        cursor.execute(f"DELETE FROM _LIST_ITEM WHERE id_list={id_list}")
        cursor.execute(f"DELETE FROM SHOPPING_LIST WHERE id_list={id_list}")

        if not no_commit:
            self.connection.commit()

    def add_product_to_list(self, id_list:int, id_product:int, quantity:int, no_commit:bool=False):
        """! Adiciona dado produto a dada lista.

        @param  id_list     ID da lista.
        @param  id_market   ID do mercado do produto.
        @param  id_product  ID do produto.
        @param  quantity    Quantidade escolhida do produto.
        """

        if not self.is_db_ok():
            return

        cursor = self.get_cursor()
        already_in_list = cursor.execute(
            f"""
            SELECT * FROM _LIST_ITEM
            WHERE id_list={id_list}
                AND id_product={id_product}
            """
        ).fetchone()

        if not already_in_list:
            cursor.execute(
                f"""
                INSERT INTO _LIST_ITEM VALUES
                ({id_list}, {id_product}, {quantity}, FALSE)
                """
            )

            if not no_commit:
                self.connection.commit()

            return True

    def remove_product_from_list(self, id_list:int, id_product:int, no_commit:bool=False):
        """! Remove produto de lista de compras.

        @param  id_list     ID da lista de compras.
        @param  id_market   ID do mercado do produto.
        @param  id_product  ID do produto a ser removido.
        """

        cursor = self.get_cursor()
        cursor.execute(
            f"""
            DELETE FROM _LIST_ITEM
            WHERE id_list={id_list}
                AND id_product={id_product}
            """)

        if not no_commit:
            self.connection.commit()

    def set_product_taken(self, id_list:int, id_product:int, taken:bool, no_commit:bool=False):
        """! Define o status do produto de lista como "pego".

        @param id_list     ID da lista.
        @param id_market   ID do mercado do produto.
        @param id_product  ID do produto.
        """

        if not self.is_db_ok():
            return

        cursor = self.get_cursor()
        cursor.execute(
            f"""
            UPDATE _LIST_ITEM
            SET taken={taken}
            WHERE id_list={id_list}
                AND id_product={id_product}
            """
        )

        if not no_commit:
            self.connection.commit()
        return True

    def create_product(
        self, name: str, id_categories: list = None, id_market: int = None, price: int = None, no_commit: bool = None
    ):
        """! Cadastra produto no BD.

        Se o produto já existir mas em outro mercado, apenas cria registro na
        tabela de relacionamento entre produto e mercado.

        @param  name       Nome do produto a ser cadastrado.
        @param  id_market  ID do mercado que oferece o produto.
        @param  price      Preço oferecido pelo produto (em centavos),
        """

        if not self.is_db_ok():
            return

        cursor = self.get_cursor()
        cursor.execute(f"INSERT INTO PRODUCT (name) VALUES ('{name}')")
        print(cursor.execute(f"select * from product where name='{name}'").fetchone())

        ## Verifica se o produto já existe pelo nome
        #cursor.execute(f"SELECT id_product FROM PRODUCT WHERE name='{name}'")
        #result = cursor.fetchone()
        #if result:
        #    id_product = result[0]
        #else:
        #    id_product = cursor.lastrowid

        #if id_categories:
        #    self.add_product_category(id_product, id_categories, no_commit)
        #if id_market:
        #    self.set_product_seller(id_product, id_market, price, no_commit)

        if not no_commit:
            self.connection.commit()

    def set_product_seller(self, id_product: int, id_market: int, price: int, no_commit: bool = None):
        """! Registra que mercado vende o produto pelo preço fornecido."""

        # Relaciona produto ao mercado e preço na tabela _MARKET_PRODUCT
        self.get_cursor().execute(
            "INSERT OR IGNORE INTO _MARKET_PRODUCT (id_market, id_product, price) VALUES (?, ?, ?)",
            (id_market, id_product, price),
        )

        if not no_commit:
            self.connection.commit()

    def add_product_category(self, id_product: int, categories: list[str], no_commit: bool = None):
        """! Adiciona categoria de produto."""

        cursor = self.get_cursor()
        for category in categories:
            # NOTE se pá isso aq quebra (⚆_⚆)
            cursor.execute(f"INSERT INTO _PRODUCT_CATEGORY VALUES ({id_product}, {category})")

        if not no_commit:
            self.connection.commit()

        # TODO #4: tranquilin
        # def add_product_review(self, id_product:int, rating:int, comment:str):
        """! Registra avaliação de produto.

        @param  id_product  ID do produto.
        @param  rating      Nota para o produto.
        @param  comment     Comentário sobre o produto.
        """

    def get_product(self, id_product: int):
        """! Busca o produto no BD e retorna todas suas informações.

        Reúne informações de ID, nome do produto e a média de suas notas.

        @param  id_product  ID do produto.

        @return Informações do produto.
        """
        if not self.is_db_ok():
            return

        query = "SELECT * FROM v_products_general WHERE id_product = ?"
        params = [id_product]

        cursor = self.get_cursor()
        cursor.execute(query, params)
        return self.format_product_search(cursor.fetchall())

    def get_product_sellers(self, id_product):
        """! Lista dos diferentes vendedores de um produto especifico, incluindo suas localizações e preços.

        @param id_product ID do produto
        """

        if not self.is_db_ok():
            return

        query = "SELECT * FROM v_product_sellers WHERE id_product = ?"
        params = [id_product]

        cursor = self.get_cursor()
        cursor.execute(query, params)
        return self.format_product_sellers(cursor.fetchall())

    def format_product_sellers(self, rows):
        """! Organiza os dados brutos de vendedores de produto em uma estrutura
        mais útil
        """

        formatted = []
        for row in rows:
            formatted.append(
                {
                    "id_product": row[0],
                    "id_market": row[1],
                    "market_name": row[2],
                    "price": row[3],
                    "market_rating": row[4],
                    "latitude": row[5],
                    "longitude": row[6],
                }
            )
        return formatted

    def get_product_reviews(self, id_product: int):
        """! Busca os Reviews de um produto.

        @param  id_product  ID do  produto.
        """

        if not self.is_db_ok():
            return
        query = "SELECT * FROM PRODUCT_REVIEW WHERE id_product = ?"
        params = [id_product]

        cursor = self.get_cursor()
        cursor.execute(query, params)
        return self.format_product_reviews(cursor.fetchall())

    def format_product_reviews(self, rows):
        """! Organiza os dados brutos de avaliações de produto em uma estrutura
        mais útil"""

        formatted = []
        for row in rows:
            formatted.append({"id_review": row[0], "rating": row[2], "comment": row[3]})
        return formatted
