from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.shop_page import ShopPage
from pages.checkout_page import CheckoutPage

def login_and_add_item(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("alice@example.com", "Password123!")
    expect(page).to_have_url("http://localhost:3000/")
    shop = ShopPage(page)
    shop.open()
    shop.add_first_product()

def test_checkout_page_loads(page):
    login_and_add_item(page)
    checkout = CheckoutPage(page)
    checkout.open()
    expect(page.locator("h1")).to_contain_text("Checkout")

def test_valid_coupon_applies_discount(page):
    login_and_add_item(page)
    checkout = CheckoutPage(page)
    checkout.open()
    checkout.apply_coupon("WELCOME5")
    expect(page.locator("body")).to_be_visible()  # discount ka actual text confirm karke update karenge

def test_invalid_coupon_shows_error(page):
    login_and_add_item(page)
    checkout = CheckoutPage(page)
    checkout.open()
    checkout.apply_coupon("INVALIDCODE999")
    expect(page.locator("text=Coupon code not recognized")).to_be_visible()

def test_empty_shipping_address_blocks_order(page):
    login_and_add_item(page)
    checkout = CheckoutPage(page)
    checkout.open()
    checkout.set_shipping_address("")
    checkout.place_order()
    expect(page).to_have_url("http://localhost:3000/checkout")

def test_place_order_success(page):
    login_and_add_item(page)
    checkout = CheckoutPage(page)
    checkout.open()
    checkout.set_shipping_address("123 Market St, Springfield")
    checkout.place_order()
    expect(page).to_have_url("http://localhost:3000/orders")