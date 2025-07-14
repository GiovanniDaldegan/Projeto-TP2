import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from modules.db_controller import DBController

db = DBController(str(Path(__file__).parent))
db.connect()
db.initialize()

def test_get_categories():
    categories = db.get_categories()
    assert len(categories) != 0
    assert type(categories[0]).__name__ == "str"

def test_search_products():
    products = db.search_products("Macarrão", {
            "min_price": 2.5,
            "max_price": 40.79,
            "category": "Mercearia"
    })

    assert len(products) != 0
    assert "id"          in products[0].keys()
    assert "name"        in products[0].keys()
    assert "rating"      in products[0].keys()
    assert "categories"  in products[0].keys()
    assert "price_range" in products[0].keys()
    assert "avg_price"   in products[0].keys()

def test_account():
    jonas = db.get_account("JONAS", "senha123")
    if jonas:
        db.delete_account(jonas["id_user"], True)

    assert db.create_account("adm", "JONAS", "senha123", True)
    assert db.account_exists("JONAS")

    acc = db.get_account("JONAS", "senha123")
    assert "id_user"  in acc.keys()
    assert "username" in acc.keys()
    assert "acc_type" in acc.keys()

def test_shopping_lists():
    db.create_shopping_list(1, "lista teste", True)

    lists = db.get_all_shopping_lists(1)
    if len(lists) != 0:
        assert "id"   in lists[0].keys()
        assert "name" in lists[0].keys()

    test_list_id = lists[-1]["id"]

    db.add_product_to_list(test_list_id, 2, 3, True)
    db.add_product_to_list(test_list_id, 5, 1, True)

    assert db.set_product_taken(test_list_id, 2, True, True)
    test_list = db.get_shopping_list(test_list_id)

    assert test_list[0]["product_id"] == 2
    assert "product_name"             in test_list[0].keys()
    assert test_list[0]["quantity"]   == 3
    assert test_list[0]["taken"]      == 1

    db.remove_product_from_list(test_list_id, 2, True)
    test_list = db.get_shopping_list(test_list_id)

    assert test_list[0]["product_id"] == 5
    assert "product_name"             in test_list[0].keys()
    assert test_list[0]["quantity"]   == 1
    assert test_list[0]["taken"]      == 0

def test_product():
    id_product = 1
    product = db.get_product(id_product)
    if len(product) != 0:
        assert "id"          in product[0].keys()
        assert "name"        in product[0].keys()
        assert "rating"      in product[0].keys()
        assert "categories"  in product[0].keys()
        assert "price_range" in product[0].keys()
        assert "avg_price"   in product[0].keys()
        
    sellers = db.get_product_sellers(id_product)    
    if len(sellers) != 0:
        assert "id_product"    in sellers[0].keys()
        assert "id_market"     in sellers[0].keys()
        assert "market_name"   in sellers[0].keys()
        assert "price"         in sellers[0].keys()
        assert "market_rating" in sellers[0].keys()
        assert "latitude"      in sellers[0].keys()
        assert "longitude"     in sellers[0].keys()

    reviews = db.get_product_reviews(id_product)
    if len(reviews) != 0:
        assert "id_review" in reviews[0].keys()
        assert "rating"    in reviews[0].keys()
        assert "comment"   in reviews[0].keys()
