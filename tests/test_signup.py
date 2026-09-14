import random
from playwright.sync_api import expect
from pages.signup_page import SignupPage

def test_valid_signup(page):
    signup = SignupPage(page)
    signup.open()
    unique_email = f"testuser{random.randint(1000,9999)}@example.com"
    signup.signup("Test User", unique_email, "Password123!")
    expect(page).to_have_url("http://localhost:3000/")

def test_duplicate_email_signup(page):
    signup = SignupPage(page)
    signup.open()
    signup.signup("Alice Duplicate", "alice@example.com", "Password123!")
    expect(page.locator("#banner")).to_be_visible()

def test_password_too_short(page):
    signup = SignupPage(page)
    signup.open()
    unique_email = f"testuser{random.randint(1000,9999)}@example.com"
    signup.signup("Test User", unique_email, "abc123")
    expect(page).to_have_url("http://localhost:3000/signup")

def test_password_boundary_8_chars(page):
    signup = SignupPage(page)
    signup.open()
    unique_email = f"testuser{random.randint(1000,9999)}@example.com"
    signup.signup("Test User", unique_email, "abcd1234")
    expect(page).to_have_url("http://localhost:3000/")

def test_empty_full_name(page):
    signup = SignupPage(page)
    signup.open()
    unique_email = f"testuser{random.randint(1000,9999)}@example.com"
    signup.signup("", unique_email, "Password123!")
    expect(page).to_have_url("http://localhost:3000/signup")

def test_invalid_email_format_signup(page):
    signup = SignupPage(page)
    signup.open()
    signup.signup("Test User", "notanemail", "Password123!")
    expect(page).to_have_url("http://localhost:3000/signup")