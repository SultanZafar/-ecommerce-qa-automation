from pages.base_page import BasePage

class CartPage(BasePage):
    URL = "http://localhost:3000/cart"

    QUANTITY_INPUT = ".qty-input"
    REMOVE_BUTTON = "button:has-text('Remove')"
    CHECKOUT_BUTTON = "#checkout-btn"
    TOTAL_TEXT = "#cart-total"

    def open(self):
        self.goto(self.URL)

    def set_quantity(self, value: str):
        self.fill(self.QUANTITY_INPUT, value)

    def remove_item(self):
        self.click(self.REMOVE_BUTTON)

    def proceed_to_checkout(self):
        self.click(self.CHECKOUT_BUTTON)