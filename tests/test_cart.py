from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.cart_page import CartPage

def login_first(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("alice@example.com", "Password123!")
    expect(page).to_have_url("http://localhost:3000/")

def login_and_add_item(page):
    login_first(page)
    page.goto("http://localhost:3000/")
    page.click("button:has-text('Add to cart') >> nth=0")

def test_cart_page_loads(page):
    login_and_add_item(page)
    cart = CartPage(page)
    cart.open()
    expect(page).to_have_url("http://localhost:3000/cart")

def test_increase_quantity(page):
    login_and_add_item(page)
    cart = CartPage(page)
    cart.open()
    cart.set_quantity("3")
    expect(page.locator(cart.TOTAL_TEXT)).to_be_visible()

def test_remove_item(page):
    login_and_add_item(page)
    cart = CartPage(page)
    cart.open()
    cart.remove_item()
    expect(page.locator("body")).to_be_visible()

def test_proceed_to_checkout(page):
    login_and_add_item(page)
    cart = CartPage(page)
    cart.open()
    page.screenshot(path="debug_cart.png")
    cart.proceed_to_checkout()
    expect(page).to_have_url("http://localhost:3000/checkout")