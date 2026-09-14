from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.shop_page import ShopPage

def login_first(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("alice@example.com", "Password123!")
    expect(page).to_have_url("http://localhost:3000/")

def test_shop_page_loads(page):
    login_first(page)
    shop = ShopPage(page)
    shop.open()
    expect(page.locator("h1")).to_contain_text("Shop all products")

def test_search_valid_product(page):
    login_first(page)
    shop = ShopPage(page)
    shop.open()
    shop.search("Headphones")
    expect(page.locator("text=Wireless Bluetooth Headphones")).to_be_visible()

def test_search_no_results(page):
    login_first(page)
    shop = ShopPage(page)
    shop.open()
    shop.search("zzz_no_such_product")
    expect(page.locator("text=Wireless Bluetooth Headphones")).not_to_be_visible()

def test_search_empty_shows_all(page):
    login_first(page)
    shop = ShopPage(page)
    shop.open()
    shop.search("")
    expect(page.locator("text=Wireless Bluetooth Headphones")).to_be_visible()

def test_add_to_cart_updates_count(page):
    login_first(page)
    shop = ShopPage(page)
    shop.open()
    shop.add_first_product()
    expect(page.locator("#nav-cart-count")).to_contain_text("1")

def test_search_case_insensitive(page):
    login_first(page)
    shop = ShopPage(page)
    shop.open()
    shop.search("headphones")
    expect(page.locator("text=Wireless Bluetooth Headphones")).to_be_visible()

def test_search_special_characters(page):
    login_first(page)
    shop = ShopPage(page)
    shop.open()
    shop.search("<script>alert(1)</script>")
    expect(page.locator("text=Wireless Bluetooth Headphones")).not_to_be_visible()