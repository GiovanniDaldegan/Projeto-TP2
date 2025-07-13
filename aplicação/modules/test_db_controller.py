import os
import shutil
import pytest
from modules.db_controller import DBController

@pytest.fixture
def temp_db(tmp_path):
    # Cria um diretório temporário para o banco de dados de teste
    db_dir = tmp_path / "databases"
    db_dir.mkdir()
    db_controller = DBController(str(tmp_path))
    db_controller.connect()
    db_controller.setup_db()
    db_controller.populate()
    yield db_controller
    db_controller.close()
    shutil.rmtree(str(tmp_path))

def test_get_categories(temp_db):
    categories = temp_db.get_categories()
    assert isinstance(categories, list)
    assert "Bebidas" in categories

def test_create_and_get_account(temp_db):
    result = temp_db.create_account("user", "testuser", "testpass")
    assert result is True
    exists = temp_db.account_exists("testuser")
    assert exists is True
    user = temp_db.get_account("testuser", "testpass")
    assert user is not None
    assert user["username"] == "testuser"

def test_create_and_get_shopping_list(temp_db):
    temp_db.create_account("user", "shopper", "1234")
    user = temp_db.get_account("shopper", "1234")
    temp_db.create_shopping_list(user["id"], "Lista Teste")
    lists = temp_db.get_all_shopping_lists(user["id"])
    assert any(l["name"] == "Lista Teste" for l in lists)

def test_add_and_remove_product_to_list(temp_db):
    # Cria usuário e lista
    temp_db.create_account("user", "shopper2", "1234")
    user = temp_db.get_account("shopper2", "1234")
    temp_db.create_shopping_list(user["id"], "Minha Lista")
    lists = temp_db.get_all_shopping_lists(user["id"])
    id_list = lists[0]["id"]
    # Adiciona produto à lista
    temp_db.add_product_to_list(id_list, 1, 2)
    shopping_list = temp_db.get_shopping_list(id_list)
    assert any(item["product_id"] == 1 for item in shopping_list)
    # Remove produto da lista
    temp_db.remove_product_from_list(id_list, 1)
    shopping_list = temp_db.get_shopping_list(id_list)
    assert not any(item["product_id"] == 1 for item in shopping_list)

def test_create_and_get_product(temp_db):
    # Cria produto e relaciona ao mercado 1
    prod_id = temp_db.create_product("Produto Teste", 1, 9.99, "img/produtos/teste.png")
    assert prod_id is not None
    produto = temp_db.get_product(prod_id)
    assert produto is not None
    assert produto[0]["name"] == "Produto Teste"
