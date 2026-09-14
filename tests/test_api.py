import requests

BASE_URL = "http://localhost:4000/api"

def test_get_products_status_ok():
    response = requests.get(f"{BASE_URL}/products?page=1&limit=12")
    assert response.status_code == 200

def test_get_products_returns_data():
    response = requests.get(f"{BASE_URL}/products?page=1&limit=12")
    data = response.json()
    assert data is not None

def test_get_categories_status_ok():
    response = requests.get(f"{BASE_URL}/products/categories")
    assert response.status_code == 200

def test_get_cart_without_auth_blocked():
    response = requests.get(f"{BASE_URL}/cart")
    assert response.status_code in (401, 403)

def test_get_orders_without_auth_blocked():
    response = requests.get(f"{BASE_URL}/orders?page=1&limit=5")
    assert response.status_code in (401, 403)

def test_get_single_product_valid_id():
    response = requests.get(f"{BASE_URL}/products/1")
    assert response.status_code == 200

def test_get_single_product_invalid_id(page=None):
    # BUG: API returns 200 instead of 404 for non-existent product ID
    response = requests.get(f"{BASE_URL}/products/99999")
    assert response.status_code == 404

def test_get_products_with_price_filter():
    response = requests.get(f"{BASE_URL}/products?minPrice=0&maxPrice=50")
    assert response.status_code == 200

def test_get_products_with_search():
    response = requests.get(f"{BASE_URL}/products?search=Headphones")
    assert response.status_code == 200

def test_get_products_invalid_page_param():
    # BUG: API returns 500 instead of 400 for invalid 'page' parameter (server crash on bad input)
    response = requests.get(f"{BASE_URL}/products?page=abc")
    assert response.status_code in (200, 400)