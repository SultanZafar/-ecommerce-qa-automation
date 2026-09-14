from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.orders_page import OrdersPage

def login_first(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("alice@example.com", "Password123!")
    expect(page).to_have_url("http://localhost:3000/")

def test_orders_page_loads(page):
    login_first(page)
    orders = OrdersPage(page)
    orders.open()
    expect(page.locator("h1")).to_contain_text("Order history")

def test_orders_list_visible(page):
    login_first(page)
    orders = OrdersPage(page)
    orders.open()
    expect(page.locator("text=PENDING").first).to_be_visible()

def test_pagination_next(page):
    login_first(page)
    orders = OrdersPage(page)
    orders.open()
    orders.click_next()
    expect(page.locator("text=Page 2 of 3")).to_be_visible()

def test_view_details_navigates(page):
    login_first(page)
    orders = OrdersPage(page)
    orders.open()
    orders.click_first_view_details()
    expect(page).not_to_have_url("http://localhost:3000/orders")