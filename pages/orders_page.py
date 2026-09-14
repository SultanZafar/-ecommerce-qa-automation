from pages.base_page import BasePage

class OrdersPage(BasePage):
    URL = "http://localhost:3000/orders"

    VIEW_DETAILS_LINK = "text=View details"
    NEXT_BUTTON = "button:has-text('Next')"
    PREVIOUS_BUTTON = "button:has-text('Previous')"

    def open(self):
        self.goto(self.URL)

    def click_next(self):
        self.click(self.NEXT_BUTTON)

    def click_previous(self):
        self.click(self.PREVIOUS_BUTTON)

    def click_first_view_details(self):
        self.page.locator(self.VIEW_DETAILS_LINK).first.click()