from pages.base_page import BasePage

class CheckoutPage(BasePage):
    URL = "http://localhost:3000/checkout"

    COUPON_INPUT = "#coupon"
    COUPON_APPLY = "button:has-text('Apply')"
    SHIPPING_ADDRESS = "textarea"
    PLACE_ORDER_BUTTON = "#place-order-btn"

    def open(self):
        self.goto(self.URL)

    def apply_coupon(self, code: str):
        self.fill(self.COUPON_INPUT, code)
        self.click(self.COUPON_APPLY)

    def set_shipping_address(self, address: str):
        self.fill(self.SHIPPING_ADDRESS, address)

    def place_order(self):
        self.click(self.PLACE_ORDER_BUTTON)