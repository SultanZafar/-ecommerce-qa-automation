from pages.base_page import BasePage

class LoginPage(BasePage):
    URL = "http://localhost:3000/login"

    EMAIL_INPUT = "input#email"
    PASSWORD_INPUT = "input#password"
    LOGIN_BUTTON = "button:has-text('log in')"
    ERROR_MESSAGE = "#banner"

    def open(self):
        self.goto(self.URL)

    def login(self,email: str, password: str):
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

