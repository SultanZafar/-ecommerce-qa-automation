from pages.base_page import BasePage

class ShopPage(BasePage):
    URL = "http://localhost:3000/"

    SEARCH_INPUT = "#search-input"
    CATEGORY_SELECT = "#category-select"
    APPLY_BUTTON = "button:has-text('Apply')"
    ADD_TO_CART_FIRST = "button:has-text('Add to cart') >> nth=0"

    def open(self):
        self.goto(self.URL)

    def search(self, text: str):
        self.fill(self.SEARCH_INPUT, text)
        self.page.keyboard.press("Enter")

    def select_category(self, value: str):
        self.page.select_option(self.CATEGORY_SELECT, label=value)

    def apply_filters(self):
        self.click(self.APPLY_BUTTON)

    def add_first_product(self):
        self.click(self.ADD_TO_CART_FIRST)