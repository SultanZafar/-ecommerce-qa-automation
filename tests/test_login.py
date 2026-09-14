from playwright.sync_api import expect
from pages.login_page import LoginPage

def test_valid_login(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("alice@example.com", "Password123!")
    expect(page).to_have_url("http://localhost:3000/")

def test_invalid_login(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("alice@example.com", "wrongpassword")
    expect(page.locator(login_page.ERROR_MESSAGE)).to_contain_text("Invalid credentials")
    
def test_empty_login(page):
    login = LoginPage(page)
    login.open()
    login.login("", "")
    assert page.url == "http://localhost:3000/login"

def test_wrong_email_valid_password(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("wrong@example.com", "Password123!")
    expect(page.locator(login_page.ERROR_MESSAGE)).to_contain_text("Invalid credentials")

def test_invalid_email_format(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("aliceexample.com", "Password123!")
    expect(page).to_have_url("http://localhost:3000/login")

def test_email_with_extra_spaces(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("  alice@example.com  ", "Password123!") 
    expect(page).to_have_url("http://localhost:3000/login")
    
def test_email_case_sensitivity(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("ALICE@EXAMPLE.COM", "Password123!")
    expect(page).to_have_url("http://localhost:3000/")

def test_sql_injection_attempt(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("' OR '1'='1", "' OR '1'='1")
    expect(page).to_have_url("http://localhost:3000/login")

def test_xss_attempt_in_email(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("<script>alert(1)</script>", "Password123!")
    expect(page).to_have_url("http://localhost:3000/login")