import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

project_root = Path(__file__).parent.parent  # Volta da pasta tests para a raiz

from modules.db_controller import DBController

def test_database():
    # 1. Inicialização
    db = DBController(project_root)
    db.connect()

    # 2. Verificação da criação do banco
    print("\n=== Verificando inicialização do banco ===")
    db.initialize()
    cursor = db.get_cursor()

    # Teste adicional: verifica se as tabelas foram criadas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("Tabelas existentes:", tables)

    # 3. Teste de população
    print("\n=== Verificando dados iniciais ===")
    cursor.execute("SELECT COUNT(*) FROM PRODUCT")
    product_count = cursor.fetchone()[0]
    print(f"Produtos cadastrados: {product_count}")

    # 4. Teste de consulta
    print("\n=== Testando consulta ===")

    filtros = {}
    #filtros["category"] ="mercearia"
    #filtros["min_price"] = 3
    #filtros["max_price"] = 5
    #filtros["min_rating"] = 4.8
    #filtros["sort"] = "rating"
    #filtros["sort"] = "min_price"


    resultados = db.search_products(filters=filtros, limit = 5)
    print("Resultados da busca por ---:", resultados)


    #5. Teste cria lista
    db.create_shopping_list("lista qualquer", 1)

    #6. Teste consulta listas
    print("\n======================\nListas apos criação:\n")
    print(db.get_all_shopping_lists(1))
    #7. Teste adicionar produto em lista
    db.add_product_to_list(3, 3, 3)
    db.add_product_to_list(3, 6, 1)
    db.add_product_to_list(3, 4, 10)
    #8. Teste consulta lista especifica
    print("\n======================\nLista apos adds:\n")
    print(db.get_shopping_list(3))

    #9. Teste set_taken
    db.set_product_taken(3, 3, 'TRUE')
    print("\n======================\nLista apos set_taken:\n")
    print(db.get_shopping_list(3))


    #10. Teste remove da lista
    db.remove_product_from_list(3, 3)
    print("\n======================\nLista apos remove:\n")
    print(db.get_shopping_list(3))

    #11. Teste get_product_sellers
    print("\n======================\nVendedores do produto 2:\n")
    print(db.get_product_sellers(2))

    #12. Teste get_product
    print("\n======================\nVProduto 2:\n")
    print(db.get_product(2))

    # 11. Fechamento
    db.close()

    # Verificação final
    assert product_count > 0, "O banco não foi populado corretamente"
    assert len(resultados) > 0, "A consulta não retornou resultados"

if __name__ == "__main__":
    test_database()