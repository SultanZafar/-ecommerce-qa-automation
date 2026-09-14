from pages.base_page import BasePage

class SignupPage(BasePage):
    URL = "http://localhost:3000/signup"

    FULL_NAME = "#name"
    EMAIL_INPUT = "#email"
    PASSWORD_INPUT = "input[type='password']"
    CREATE_ACCOUNT_BUTTON = "button:has-text('Create account')"

    def open(self):
        self.goto(self.URL)

    def signup(self, name: str, email: str, password: str):
        self.fill(self.FULL_NAME, name)
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.CREATE_ACCOUNT_BUTTON)
