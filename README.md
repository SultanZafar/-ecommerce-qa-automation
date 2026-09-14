# E-Commerce QA Automation Framework

Automated testing suite for a full-stack e-commerce web application, built using **Python + Playwright** with the **Page Object Model (POM)** design pattern.

## Tech Stack
- **Language:** Python
- **UI Automation:** Playwright (sync API)
- **API Testing:** Python `requests` library
- **Test Runner:** pytest
- **Bug Tracking:** Jira

## Test Coverage — 45 Automated Tests
| Module | Tests | Coverage |
|---|---|---|
| Login | 9 | Valid/invalid credentials, SQL injection, XSS, boundary cases |
| Signup | 6 | Duplicate email, password boundaries, empty fields |
| Shop / Product Listing | 7 | Search, category filter, add to cart, XSS in search |
| Cart | 4 | Quantity update, remove item, checkout navigation |
| Checkout | 5 | Coupon codes, shipping address validation, order placement |
| My Orders | 4 | Order history, pagination, order details |
| API (REST) | 10 | Status codes, auth-protected endpoints, negative/boundary testing |

## Framework Design
- **Page Object Model:** each page has its own class (locators + actions), inheriting shared methods from a `BasePage`.
- **Auto-waiting assertions:** Playwright's `expect()` used throughout to avoid flaky tests from timing issues.
- **Test isolation:** each test independently sets up its own required state (login, cart items) rather than depending on execution order.

## Bugs Found During Testing
1. `GET /api/products/{id}` returns `200 OK` instead of `404 Not Found` for a non-existent product ID.
2. `GET /api/products?page=abc` causes a `500 Internal Server Error` instead of `400 Bad Request` — indicates missing input validation.

Both logged and tracked in Jira with steps to reproduce, severity, and priority.

## Running the Tests
```bash
pip install -r requirements.txt
playwright install
pytest tests/ -v --headed
```