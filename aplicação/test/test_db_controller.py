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
    
    # Teste adicional: verifica se as tabelas foram criadas
    db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = db.cursor.fetchall()
    print("Tabelas existentes:", tables)
    
    # 3. Teste de população
    print("\n=== Verificando dados iniciais ===")
    db.cursor.execute("SELECT COUNT(*) FROM PRODUCT")
    product_count = db.cursor.fetchone()[0]
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


    resultados = db.search_products(filters=filtros)
    print("Resultados da busca por ---:", resultados)
    
    # 5. Fechamento
    db.close()
    
    # Verificação final
    assert product_count > 0, "O banco não foi populado corretamente"
    assert len(resultados) > 0, "A consulta não retornou resultados"

if __name__ == "__main__":
    test_database()